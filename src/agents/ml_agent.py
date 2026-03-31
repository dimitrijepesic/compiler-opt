# src/agents/ml_agent.py

import numpy as np
import compiler_gym
import json
import os
import pickle
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False


class MLAgent:
    """
    Machine Learning agent using traditional ML models.
    """

    def __init__(self, benchmark, model_type="random_forest"):
        self.benchmark = benchmark
        self.model_type = model_type
        self.model = None
        self.label_encoder = LabelEncoder()
        
        # Environment for evaluation
        self.env = compiler_gym.make("llvm-ic-v0")
        self.env.reset(benchmark=benchmark)
        self.num_actions = self.env.action_space.n
        
        self.best_score = None
        self.best_sequence = []
        
        # Store action mapping
        self.classes_ = None

    def _create_model(self):
        """Create the ML model."""
        if self.model_type == "random_forest":
            return RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=10,
                min_samples_leaf=5,
                max_features='sqrt',
                n_jobs=-1,
                random_state=42
            )
        elif self.model_type == "xgboost":
            return XGBClassifier(
                n_estimators=200,
                max_depth=8,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                n_jobs=-1,
                random_state=42,
                verbosity=0,
                use_label_encoder=False,
                eval_metric='mlogloss'
            )
        elif self.model_type == "knn":
            return KNeighborsClassifier(
                n_neighbors=10,
                weights='distance',
                n_jobs=-1
            )
        elif self.model_type == "gradient_boosting":
            return GradientBoostingClassifier(
                n_estimators=100,
                max_depth=8,
                learning_rate=0.1,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model: {self.model_type}")

    def load_data(self, data_path="data/greedy_trajectories.json"):
        """Load pre-collected training data."""
        print(f"   Loading data from {data_path}...")
        
        with open(data_path, "r") as f:
            raw_data = json.load(f)
        
        features = np.array([d["features"] for d in raw_data], dtype=np.float32)
        actions = np.array([d["action"] for d in raw_data], dtype=np.int64)
        
        unique_actions = np.unique(actions)
        print(f"   Loaded {len(features)} samples, {len(unique_actions)} unique actions")
        print(f"   Actions: {unique_actions[:10]}..." if len(unique_actions) > 10 else f"   Actions: {unique_actions}")
        
        return features, actions

    def train_model(self, features, actions):
        """Train the ML model."""
        print(f"   Training {self.model_type}...")
        
        # Encode actions to 0, 1, 2, ... (required for XGBoost)
        actions_encoded = self.label_encoder.fit_transform(actions)
        self.classes_ = self.label_encoder.classes_
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            features, actions_encoded, test_size=0.2, random_state=42, stratify=actions_encoded
        )
        
        print(f"   Train: {len(X_train)}, Val: {len(X_val)}")
        
        # Create and train model
        self.model = self._create_model()
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_pred = self.model.predict(X_train)
        val_pred = self.model.predict(X_val)
        
        train_acc = accuracy_score(y_train, train_pred)
        val_acc = accuracy_score(y_val, val_pred)
        
        print(f"   Train accuracy: {train_acc:.1%}")
        print(f"   Val accuracy: {val_acc:.1%}")
        
        # Top-k accuracy
        if hasattr(self.model, 'predict_proba'):
            val_proba = self.model.predict_proba(X_val)
            top3 = self._top_k_accuracy(val_proba, y_val, k=3)
            top5 = self._top_k_accuracy(val_proba, y_val, k=5)
            print(f"   Val top-3 accuracy: {top3:.1%}")
            print(f"   Val top-5 accuracy: {top5:.1%}")
        
        # Feature importance
        if hasattr(self.model, 'feature_importances_'):
            self._print_feature_importance()
        
        return val_acc

    def _top_k_accuracy(self, proba, y_true, k=5):
        """Calculate top-k accuracy."""
        top_k_preds = np.argsort(proba, axis=1)[:, -k:]
        correct = sum(y in preds for y, preds in zip(y_true, top_k_preds))
        return correct / len(y_true)

    def _print_feature_importance(self, top_n=10):
        """Print most important features."""
        importance = self.model.feature_importances_
        
        feature_names = [
            "BBNumArgsHi", "BBNumArgsLo", "onePred", "onePredOneSuc", 
            "onePredTwoSuc", "oneSuccessor", "twoPred", "twoPredOneSuc",
            "twoEach", "twoSuccessor", "morePreds", "worePredOneSuc",
            "worePredTwoSuc", "morePredMoreSuc", "NumEdges", "NumCritEdges",
            "BranchCount", "NumBB", "returnCount", "PhiCount", 
            "BlockLow", "BlockMid", "BlockHi", "ArithCount",
            "CallCount", "BitwiseCount", "CompareCount", "ShiftCount",
            "UnaryCount", "FPArithCount", "FPCompareCount", "LoadCount",
            "StoreCount", "AllocaCount", "SelectCount", "GetElemPtrCount",
            "CastCount", "VarArgCount", "ExtractElemCount", "InsertElemCount",
            "ShuffleVecCount", "ExtractValCount", "InsertValCount", "LandPadCount",
            "FenceCount", "AtomicRMWCount", "AtomicCmpXchgCount", "VAArgCount",
            "UnknownInst", "TotalInsts", "TotalBlocks", "TotalFuncs",
            "TotalMemInst", "BeginPhi", "ArgsPhi", "UnknownFeat"
        ]
        
        indices = np.argsort(importance)[::-1][:top_n]
        
        print(f"\n   Top {top_n} important features:")
        for i, idx in enumerate(indices):
            name = feature_names[idx] if idx < len(feature_names) else f"Feature_{idx}"
            print(f"      {i+1}. {name}: {importance[idx]:.4f}")

    def predict(self, features):
        """Predict best action for given features."""
        features = np.array(features).reshape(1, -1)
        
        if hasattr(self.model, 'predict_proba'):
            # Get probabilities and sample from top-k
            proba = self.model.predict_proba(features)[0]
            
            # Get top 3 predictions
            top_k_idx = np.argsort(proba)[-3:][::-1]
            
            # Return the best one (highest probability)
            encoded_action = top_k_idx[0]
        else:
            encoded_action = self.model.predict(features)[0]
        
        # Decode back to original action
        original_action = self.classes_[encoded_action]
        return original_action

    def evaluate(self, steps=45):
        """Run trained model on target benchmark."""
        print("   Evaluating...")
        
        self.env.reset(benchmark=self.benchmark)
        initial_ic = self.env.observation["IrInstructionCount"]
        actions_taken = []
        
        for step in range(steps):
            try:
                autophase = self.env.observation["Autophase"]
                features = np.log1p(np.array(autophase, dtype=np.float32))
            except:
                break
            
            action = self.predict(features)
            
            try:
                self.env.step(int(action))
                actions_taken.append(int(action))
            except:
                continue
        
        final_ic = self.env.observation["IrInstructionCount"]
        return final_ic, actions_taken, initial_ic

    def train(self, data_path="data/greedy_trajectories.json"):
        """Full training pipeline."""
        print(f"-- ML Agent ({self.model_type}) na {self.benchmark}")
        
        # Load data
        features, actions = self.load_data(data_path)
        
        # Train
        val_acc = self.train_model(features, actions)
        
        # Evaluate
        final_ic, actions_taken, initial_ic = self.evaluate()
        
        self.best_score = final_ic
        self.best_sequence = actions_taken
        
        reduction = (initial_ic - final_ic) / initial_ic * 100
        print(f"\n   Rezultat: {initial_ic} -> {final_ic} ({reduction:.1f}% redukcija)")
        
        return self.best_score, self.best_sequence

    def close(self):
        self.env.close()


def compare_models(data_path="data/greedy_trajectories.json"):
    """Compare different ML models."""
    
    print("=" * 70)
    print("COMPARING ML MODELS")
    print("=" * 70)
    
    benchmark = "benchmark://cbench-v1/qsort"
    results = {}
    
    models_to_test = ["random_forest", "knn", "gradient_boosting"]
    if HAS_XGB:
        models_to_test.append("xgboost")
    
    for model_type in models_to_test:
        print(f"\n{'='*70}")
        print(f"MODEL: {model_type.upper()}")
        print(f"{'='*70}")
        
        try:
            agent = MLAgent(benchmark, model_type=model_type)
            score, _ = agent.train(data_path)
            agent.close()
            results[model_type] = score
        except Exception as e:
            print(f"   Error: {e}")
            results[model_type] = None
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    print(f"\n{'Model':<20} {'Score':>10} {'vs -O3 (289)':>15}")
    print("-" * 50)
    
    for model, score in sorted(results.items(), key=lambda x: x[1] if x[1] else 9999):
        if score:
            vs_o3 = (289 - score) / 289 * 100
            print(f"{model:<20} {score:>10} {vs_o3:>+14.1f}%")
        else:
            print(f"{model:<20} {'FAILED':>10}")
    
    print(f"\n{'Greedy':<20} {'271':>10} {'+6.2%':>15}")
    print(f"{'-O3':<20} {'289':>10} {'baseline':>15}")
    
    valid_results = {k: v for k, v in results.items() if v}
    if valid_results:
        best_model = min(valid_results, key=valid_results.get)
        print(f"\nBest model: {best_model} ({valid_results[best_model]})")
    
    return results


def run_on_all_benchmarks(model_type="random_forest", data_path="data/greedy_trajectories.json"):
    """Run best model on all benchmarks."""
    
    BENCHMARKS = [
        ("qsort", 289, 271),
        ("crc32", 122, 114),
        ("dijkstra", 275, 258),
        ("adpcm", 221, 218),
        ("sha", 427, 358),
    ]
    
    print("=" * 70)
    print(f"RUNNING {model_type.upper()} ON ALL BENCHMARKS")
    print("=" * 70)
    
    # Load data once and train model
    with open(data_path, "r") as f:
        raw_data = json.load(f)
    
    features = np.array([d["features"] for d in raw_data], dtype=np.float32)
    actions = np.array([d["action"] for d in raw_data], dtype=np.int64)
    
    # Create and train model
    agent = MLAgent("benchmark://cbench-v1/qsort", model_type=model_type)
    
    # Encode labels
    actions_encoded = agent.label_encoder.fit_transform(actions)
    agent.classes_ = agent.label_encoder.classes_
    agent.model = agent._create_model()
    agent.model.fit(features, actions_encoded)
    
    print(f"\nModel trained on {len(features)} samples")
    
    # Test on each benchmark
    print(f"\n{'Benchmark':<15} {'O3':>8} {'Greedy':>8} {'ML':>8} {'vs O3':>10} {'vs Greedy':>12}")
    print("-" * 70)
    
    total_o3 = 0
    total_greedy = 0
    total_ml = 0
    
    for name, o3, greedy in BENCHMARKS:
        benchmark = f"benchmark://cbench-v1/{name}"
        
        agent.env.reset(benchmark=benchmark)
        initial_ic = agent.env.observation["IrInstructionCount"]
        
        for step in range(45):
            try:
                autophase = agent.env.observation["Autophase"]
                features_step = np.log1p(np.array(autophase, dtype=np.float32))
                action = agent.predict(features_step)
                agent.env.step(int(action))
            except:
                continue
        
        ml_score = agent.env.observation["IrInstructionCount"]
        
        vs_o3 = (o3 - ml_score) / o3 * 100
        vs_greedy = (greedy - ml_score) / greedy * 100
        
        print(f"{name:<15} {o3:>8} {greedy:>8} {ml_score:>8} {vs_o3:>+9.1f}% {vs_greedy:>+11.1f}%")
        
        total_o3 += o3
        total_greedy += greedy
        total_ml += ml_score
    
    print("-" * 70)
    vs_o3_total = (total_o3 - total_ml) / total_o3 * 100
    vs_greedy_total = (total_greedy - total_ml) / total_greedy * 100
    print(f"{'TOTAL':<15} {total_o3:>8} {total_greedy:>8} {total_ml:>8} {vs_o3_total:>+9.1f}% {vs_greedy_total:>+11.1f}%")
    
    agent.close()


if __name__ == "__main__":
    if not os.path.exists("data/greedy_trajectories.json"):
        print("Data not found. Run: python src/data/collect_and_save.py")
        exit(1)
    
    # Compare models
    results = compare_models()
    
    # Run best model on all benchmarks
    print("\n")
    run_on_all_benchmarks(model_type="random_forest")