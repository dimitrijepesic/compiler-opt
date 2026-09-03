from .base_agent import OptimizerAgent


class GreedyAgent(OptimizerAgent):
    """Demo greedy search used by scripts/demo_runner.py only, capped at
    `steps` iterations. The paper's reference greedy search
    (results/full_baselines_v2.json) has no step cap: it tries every pass
    at every step and stops only when none improves."""

    def train(self, steps=15):
        print(f"-- running greedy agent on {self.env.benchmark}")
        self.env.reset()

        current_size = self.env.observation["IrInstructionCount"]
        print(f"start: {current_size}")

        self.update_best(current_size, [])
        actions_taken = []

        for step in range(1, steps + 1):
            print(f"\n-- step {step}/{steps}")
            best_action = None
            best_reduction = 0
            best_new_size = current_size

            for action in range(self.env.action_space.n):
                try:
                    with self.env.fork() as temp_env:
                        temp_env.step(action)
                        # Get observation from the environment, not from step() return
                        observation = temp_env.observation["IrInstructionCount"]

                        if observation is None:
                            continue

                        if observation < best_new_size:
                            best_new_size = observation
                            best_action = action
                            best_reduction = current_size - best_new_size
                except Exception:
                    # Some actions may fail; skip them
                    continue

            if best_action is not None and best_reduction > 0:
                action_name = self.env.action_space.to_string(best_action)
                print(f"  Best action: {action_name}")
                print(f"  Reduction: {current_size} -> {best_new_size} (delta: -{best_reduction})")

                self.env.step(best_action)
                current_size = self.env.observation["IrInstructionCount"]
                actions_taken.append(best_action)

                self.update_best(current_size, actions_taken.copy())

                self.history.append({
                    "step": step,
                    "size": int(current_size),
                    "action_id": int(best_action),
                    "action_name": action_name,
                })
            else:
                print("  No action reduces the code further. Local minimum.")
                break

        print("\n" + "=" * 40)
        print(f"GREEDY FINISHED. Best result: {self.best_score}")
        print(f"Sequence: {self.best_sequence}")
