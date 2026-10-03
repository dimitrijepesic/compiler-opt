source_filename = "-"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@tmult = external global [8800 x [5 x [5 x [5 x double]]]], align 16
@ntot = external local_unnamed_addr global i32, align 4
@nelt = external local_unnamed_addr global i32, align 4
@idel = external local_unnamed_addr global [8800 x [6 x [5 x [5 x i32]]]], align 16
@idmo = external local_unnamed_addr global [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], align 16
@cbc = external local_unnamed_addr global [8800 x [6 x i32]], align 16
@v_end = external local_unnamed_addr global [2 x i32], align 4
@qbnew = external local_unnamed_addr global [2 x [5 x [3 x double]]], align 16
@nmor = external local_unnamed_addr global i32, align 4
@tmort = external global [334600 x double], align 16
@mormult = external global [334600 x double], align 16

; Function Attrs: nounwind uwtable
define void @transf(double* nocapture readonly %tmor, double* %tx) local_unnamed_addr #0 {
  %tmp = alloca [2 x [5 x [5 x double]]], align 16
  %1 = load i32, i32* @ntot, align 4
  tail call void @col2(double* %tx, double* getelementptr inbounds ([8800 x [5 x [5 x [5 x double]]]], [8800 x [5 x [5 x [5 x double]]]]* @tmult, i64 0, i64 0, i64 0, i64 0, i64 0), i32 %1) #4
  %2 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 0, i64 0, i64 0
  br label %3

3:                                                ; preds = %1088, %0
  %indvars.iv264 = phi i64 [ %indvars.iv.next265, %1088 ], [ 0, %0 ]
  %4 = load i32, i32* @nelt, align 4
  %5 = sext i32 %4 to i64
  %6 = icmp slt i64 %indvars.iv264, %5
  br i1 %6, label %.preheader29, label %1089

.preheader29:                                     ; preds = %.loopexit, %3
  %indvars.iv261 = phi i64 [ %indvars.iv.next262, %.loopexit ], [ 0, %3 ]
  %exitcond263 = icmp eq i64 %indvars.iv261, 6
  br i1 %exitcond263, label %1088, label %7

7:                                                ; preds = %.preheader29
  %8 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0
  %9 = load i32, i32* %8, align 4
  %10 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 4
  %11 = load i32, i32* %10, align 4
  %12 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 4, i64 0
  %13 = load i32, i32* %12, align 4
  %14 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 4, i64 4
  %15 = load i32, i32* %14, align 4
  %16 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 0, i64 0
  %17 = load i32, i32* %16, align 16
  %18 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 0, i64 0, i64 4
  %19 = load i32, i32* %18, align 8
  %20 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 1, i64 4, i64 0
  %21 = load i32, i32* %20, align 4
  %22 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 1, i64 4, i64 4
  %23 = load i32, i32* %22, align 4
  %24 = sext i32 %17 to i64
  %25 = getelementptr inbounds double, double* %tmor, i64 %24
  %26 = bitcast double* %25 to i64*
  %27 = load i64, i64* %26, align 8
  %28 = sext i32 %9 to i64
  %29 = getelementptr inbounds double, double* %tx, i64 %28
  %30 = bitcast double* %29 to i64*
  store i64 %27, i64* %30, align 8
  %31 = sext i32 %19 to i64
  %32 = getelementptr inbounds double, double* %tmor, i64 %31
  %33 = bitcast double* %32 to i64*
  %34 = load i64, i64* %33, align 8
  %35 = sext i32 %11 to i64
  %36 = getelementptr inbounds double, double* %tx, i64 %35
  %37 = bitcast double* %36 to i64*
  store i64 %34, i64* %37, align 8
  %38 = sext i32 %21 to i64
  %39 = getelementptr inbounds double, double* %tmor, i64 %38
  %40 = bitcast double* %39 to i64*
  %41 = load i64, i64* %40, align 8
  %42 = sext i32 %13 to i64
  %43 = getelementptr inbounds double, double* %tx, i64 %42
  %44 = bitcast double* %43 to i64*
  store i64 %41, i64* %44, align 8
  %45 = sext i32 %23 to i64
  %46 = getelementptr inbounds double, double* %tmor, i64 %45
  %47 = bitcast double* %46 to i64*
  %48 = load i64, i64* %47, align 8
  %49 = sext i32 %15 to i64
  %50 = getelementptr inbounds double, double* %tx, i64 %49
  %51 = bitcast double* %50 to i64*
  store i64 %48, i64* %51, align 8
  %52 = getelementptr inbounds [8800 x [6 x i32]], [8800 x [6 x i32]]* @cbc, i64 0, i64 %indvars.iv264, i64 %indvars.iv261
  %53 = load i32, i32* %52, align 4
  %54 = icmp eq i32 %53, 3
  br i1 %54, label %55, label %.preheader28.1

55:                                               ; preds = %7
  call void @r_init(double* nonnull %2, i32 50, double 0.000000e+00) #4
  br label %56

56:                                               ; preds = %165, %55
  %indvars.iv222 = phi i64 [ %indvars.iv.next223, %165 ], [ 0, %55 ]
  %exitcond225 = icmp eq i64 %indvars.iv222, 2
  br i1 %exitcond225, label %.preheader11.preheader, label %.preheader9

.preheader11.preheader:                           ; preds = %56
  %57 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 0
  %58 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 2, i64 0
  %59 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 3, i64 0
  %60 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 4
  %61 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 2, i64 4
  %62 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 3, i64 4
  br label %.preheader11

.preheader9:                                      ; preds = %164, %56
  %indvars.iv219 = phi i64 [ %indvars.iv.next220, %164 ], [ 0, %56 ]
  %exitcond221 = icmp eq i64 %indvars.iv219, 2
  br i1 %exitcond221, label %165, label %.preheader1

.preheader1:                                      ; preds = %.preheader9
  %63 = getelementptr inbounds [2 x i32], [2 x i32]* @v_end, i64 0, i64 %indvars.iv219
  %64 = load i32, i32* %63, align 4
  %65 = sext i32 %64 to i64
  %66 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 0, i64 0
  %67 = load double, double* %66, align 8
  %68 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 1, i64 0
  %69 = load double, double* %68, align 8
  %70 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 2, i64 0
  %71 = load double, double* %70, align 8
  %72 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 3, i64 0
  %73 = load double, double* %72, align 8
  %74 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 4, i64 0
  %75 = load double, double* %74, align 8
  %76 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 0, i64 1
  %77 = load double, double* %76, align 8
  %78 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 1, i64 1
  %79 = load double, double* %78, align 8
  %80 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 2, i64 1
  %81 = load double, double* %80, align 8
  %82 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 3, i64 1
  %83 = load double, double* %82, align 8
  %84 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 4, i64 1
  %85 = load double, double* %84, align 8
  %86 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 0, i64 2
  %87 = load double, double* %86, align 8
  %88 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 1, i64 2
  %89 = load double, double* %88, align 8
  %90 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 2, i64 2
  %91 = load double, double* %90, align 8
  %92 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 3, i64 2
  %93 = load double, double* %92, align 8
  %94 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv219, i64 4, i64 2
  %95 = load double, double* %94, align 8
  br label %96

96:                                               ; preds = %97, %.preheader1
  %indvars.iv216 = phi i64 [ 0, %.preheader1 ], [ %indvars.iv.next217, %97 ]
  %exitcond218 = icmp eq i64 %indvars.iv216, 5
  br i1 %exitcond218, label %164, label %97

97:                                               ; preds = %96
  %98 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 %indvars.iv219, i64 %indvars.iv222, i64 %indvars.iv216, i64 %65
  %99 = load i32, i32* %98, align 4
  %100 = sext i32 %99 to i64
  %101 = getelementptr inbounds double, double* %tmor, i64 %100
  %102 = bitcast double* %101 to i64*
  %103 = load i64, i64* %102, align 8
  %104 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv222, i64 %indvars.iv216, i64 %65
  %105 = bitcast double* %104 to i64*
  store i64 %103, i64* %105, align 8
  %106 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 %indvars.iv219, i64 %indvars.iv222, i64 %indvars.iv216, i64 0
  %107 = load i32, i32* %106, align 4
  %108 = sext i32 %107 to i64
  %109 = getelementptr inbounds double, double* %tmor, i64 %108
  %110 = load double, double* %109, align 8
  %111 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 %indvars.iv219, i64 %indvars.iv222, i64 %indvars.iv216, i64 1
  %112 = load i32, i32* %111, align 4
  %113 = sext i32 %112 to i64
  %114 = getelementptr inbounds double, double* %tmor, i64 %113
  %115 = load double, double* %114, align 8
  %116 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 %indvars.iv219, i64 %indvars.iv222, i64 %indvars.iv216, i64 2
  %117 = load i32, i32* %116, align 4
  %118 = sext i32 %117 to i64
  %119 = getelementptr inbounds double, double* %tmor, i64 %118
  %120 = load double, double* %119, align 8
  %121 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 %indvars.iv219, i64 %indvars.iv222, i64 %indvars.iv216, i64 3
  %122 = load i32, i32* %121, align 4
  %123 = sext i32 %122 to i64
  %124 = getelementptr inbounds double, double* %tmor, i64 %123
  %125 = load double, double* %124, align 8
  %126 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 %indvars.iv219, i64 %indvars.iv222, i64 %indvars.iv216, i64 4
  %127 = load i32, i32* %126, align 4
  %128 = sext i32 %127 to i64
  %129 = getelementptr inbounds double, double* %tmor, i64 %128
  %130 = load double, double* %129, align 8
  %131 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv222, i64 %indvars.iv216, i64 1
  %.promoted = load double, double* %131, align 8
  %132 = fmul double %67, %110
  %133 = fadd double %.promoted, %132
  %134 = fmul double %69, %115
  %135 = fadd double %133, %134
  %136 = fmul double %71, %120
  %137 = fadd double %135, %136
  %138 = fmul double %73, %125
  %139 = fadd double %137, %138
  %140 = fmul double %75, %130
  %141 = fadd double %139, %140
  store double %141, double* %131, align 8
  %142 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv222, i64 %indvars.iv216, i64 2
  %.promoted.1 = load double, double* %142, align 8
  %143 = fmul double %77, %110
  %144 = fadd double %.promoted.1, %143
  %145 = fmul double %79, %115
  %146 = fadd double %144, %145
  %147 = fmul double %81, %120
  %148 = fadd double %146, %147
  %149 = fmul double %83, %125
  %150 = fadd double %148, %149
  %151 = fmul double %85, %130
  %152 = fadd double %150, %151
  store double %152, double* %142, align 8
  %153 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv222, i64 %indvars.iv216, i64 3
  %.promoted.2 = load double, double* %153, align 8
  %154 = fmul double %87, %110
  %155 = fadd double %.promoted.2, %154
  %156 = fmul double %89, %115
  %157 = fadd double %155, %156
  %158 = fmul double %91, %120
  %159 = fadd double %157, %158
  %160 = fmul double %93, %125
  %161 = fadd double %159, %160
  %162 = fmul double %95, %130
  %163 = fadd double %161, %162
  store double %163, double* %153, align 8
  %indvars.iv.next217 = add nuw nsw i64 %indvars.iv216, 1
  br label %96

164:                                              ; preds = %96
  %indvars.iv.next220 = add nuw nsw i64 %indvars.iv219, 1
  br label %.preheader9

165:                                              ; preds = %.preheader9
  %indvars.iv.next223 = add nuw nsw i64 %indvars.iv222, 1
  br label %56

.preheader11:                                     ; preds = %.preheader6, %.preheader11.preheader
  %indvars.iv257 = phi i64 [ %indvars.iv.next258, %.preheader6 ], [ 0, %.preheader11.preheader ]
  %exitcond260 = icmp eq i64 %indvars.iv257, 2
  br i1 %exitcond260, label %.loopexit, label %.preheader8

.preheader8:                                      ; preds = %.preheader11
  %166 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 0, i64 0
  %167 = load double, double* %166, align 8
  %168 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 1, i64 0
  %169 = load double, double* %168, align 8
  %170 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 2, i64 0
  %171 = load double, double* %170, align 8
  %172 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 3, i64 0
  %173 = load double, double* %172, align 8
  %174 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 4, i64 0
  %175 = load double, double* %174, align 8
  %176 = load i32, i32* %57, align 4
  %177 = sext i32 %176 to i64
  %178 = getelementptr inbounds double, double* %tx, i64 %177
  %179 = load double, double* %178, align 8
  %180 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 0, i64 0
  %181 = load double, double* %180, align 8
  %182 = fmul double %181, %167
  %183 = fmul double %182, 5.000000e-01
  %184 = fadd double %179, %183
  store double %184, double* %178, align 8
  %185 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 1, i64 0
  %186 = load double, double* %185, align 8
  %187 = fmul double %186, %169
  %188 = fmul double %187, 5.000000e-01
  %189 = fadd double %184, %188
  store double %189, double* %178, align 8
  %190 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 2, i64 0
  %191 = load double, double* %190, align 8
  %192 = fmul double %191, %171
  %193 = fmul double %192, 5.000000e-01
  %194 = fadd double %189, %193
  store double %194, double* %178, align 8
  %195 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 3, i64 0
  %196 = load double, double* %195, align 8
  %197 = fmul double %196, %173
  %198 = fmul double %197, 5.000000e-01
  %199 = fadd double %194, %198
  store double %199, double* %178, align 8
  %200 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 4, i64 0
  %201 = load double, double* %200, align 8
  %202 = fmul double %201, %175
  %203 = fmul double %202, 5.000000e-01
  %204 = fadd double %199, %203
  store double %204, double* %178, align 8
  %205 = load i32, i32* %58, align 4
  %206 = sext i32 %205 to i64
  %207 = getelementptr inbounds double, double* %tx, i64 %206
  %208 = load double, double* %207, align 8
  %209 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 0, i64 1
  %210 = load double, double* %209, align 8
  %211 = fmul double %210, %167
  %212 = fmul double %211, 5.000000e-01
  %213 = fadd double %208, %212
  store double %213, double* %207, align 8
  %214 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 1, i64 1
  %215 = load double, double* %214, align 8
  %216 = fmul double %215, %169
  %217 = fmul double %216, 5.000000e-01
  %218 = fadd double %213, %217
  store double %218, double* %207, align 8
  %219 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 2, i64 1
  %220 = load double, double* %219, align 8
  %221 = fmul double %220, %171
  %222 = fmul double %221, 5.000000e-01
  %223 = fadd double %218, %222
  store double %223, double* %207, align 8
  %224 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 3, i64 1
  %225 = load double, double* %224, align 8
  %226 = fmul double %225, %173
  %227 = fmul double %226, 5.000000e-01
  %228 = fadd double %223, %227
  store double %228, double* %207, align 8
  %229 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 4, i64 1
  %230 = load double, double* %229, align 8
  %231 = fmul double %230, %175
  %232 = fmul double %231, 5.000000e-01
  %233 = fadd double %228, %232
  store double %233, double* %207, align 8
  %234 = load i32, i32* %59, align 4
  %235 = sext i32 %234 to i64
  %236 = getelementptr inbounds double, double* %tx, i64 %235
  %237 = load double, double* %236, align 8
  %238 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 0, i64 2
  %239 = load double, double* %238, align 8
  %240 = fmul double %239, %167
  %241 = fmul double %240, 5.000000e-01
  %242 = fadd double %237, %241
  store double %242, double* %236, align 8
  %243 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 1, i64 2
  %244 = load double, double* %243, align 8
  %245 = fmul double %244, %169
  %246 = fmul double %245, 5.000000e-01
  %247 = fadd double %242, %246
  store double %247, double* %236, align 8
  %248 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 2, i64 2
  %249 = load double, double* %248, align 8
  %250 = fmul double %249, %171
  %251 = fmul double %250, 5.000000e-01
  %252 = fadd double %247, %251
  store double %252, double* %236, align 8
  %253 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 3, i64 2
  %254 = load double, double* %253, align 8
  %255 = fmul double %254, %173
  %256 = fmul double %255, 5.000000e-01
  %257 = fadd double %252, %256
  store double %257, double* %236, align 8
  %258 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv257, i64 4, i64 2
  %259 = load double, double* %258, align 8
  %260 = fmul double %259, %175
  %261 = fmul double %260, 5.000000e-01
  %262 = fadd double %257, %261
  store double %262, double* %236, align 8
  %263 = getelementptr inbounds [2 x i32], [2 x i32]* @v_end, i64 0, i64 %indvars.iv257
  br label %264

264:                                              ; preds = %347, %.preheader8
  %indvars.iv245 = phi i64 [ 1, %.preheader8 ], [ %indvars.iv.next246, %347 ]
  %exitcond247 = icmp eq i64 %indvars.iv245, 4
  br i1 %exitcond247, label %.preheader6, label %347

.preheader6:                                      ; preds = %264
  %265 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 0, i64 4
  %266 = load double, double* %265, align 8
  %267 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 1, i64 4
  %268 = load double, double* %267, align 8
  %269 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 2, i64 4
  %270 = load double, double* %269, align 8
  %271 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 3, i64 4
  %272 = load double, double* %271, align 8
  %273 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 4, i64 4
  %274 = load double, double* %273, align 8
  %275 = load i32, i32* %60, align 4
  %276 = sext i32 %275 to i64
  %277 = getelementptr inbounds double, double* %tx, i64 %276
  %278 = load double, double* %277, align 8
  %279 = load double, double* %180, align 8
  %280 = fmul double %279, %266
  %281 = fmul double %280, 5.000000e-01
  %282 = fadd double %278, %281
  store double %282, double* %277, align 8
  %283 = load double, double* %185, align 8
  %284 = fmul double %283, %268
  %285 = fmul double %284, 5.000000e-01
  %286 = fadd double %282, %285
  store double %286, double* %277, align 8
  %287 = load double, double* %190, align 8
  %288 = fmul double %287, %270
  %289 = fmul double %288, 5.000000e-01
  %290 = fadd double %286, %289
  store double %290, double* %277, align 8
  %291 = load double, double* %195, align 8
  %292 = fmul double %291, %272
  %293 = fmul double %292, 5.000000e-01
  %294 = fadd double %290, %293
  store double %294, double* %277, align 8
  %295 = load double, double* %200, align 8
  %296 = fmul double %295, %274
  %297 = fmul double %296, 5.000000e-01
  %298 = fadd double %294, %297
  store double %298, double* %277, align 8
  %299 = load i32, i32* %61, align 4
  %300 = sext i32 %299 to i64
  %301 = getelementptr inbounds double, double* %tx, i64 %300
  %302 = load double, double* %301, align 8
  %303 = load double, double* %209, align 8
  %304 = fmul double %303, %266
  %305 = fmul double %304, 5.000000e-01
  %306 = fadd double %302, %305
  store double %306, double* %301, align 8
  %307 = load double, double* %214, align 8
  %308 = fmul double %307, %268
  %309 = fmul double %308, 5.000000e-01
  %310 = fadd double %306, %309
  store double %310, double* %301, align 8
  %311 = load double, double* %219, align 8
  %312 = fmul double %311, %270
  %313 = fmul double %312, 5.000000e-01
  %314 = fadd double %310, %313
  store double %314, double* %301, align 8
  %315 = load double, double* %224, align 8
  %316 = fmul double %315, %272
  %317 = fmul double %316, 5.000000e-01
  %318 = fadd double %314, %317
  store double %318, double* %301, align 8
  %319 = load double, double* %229, align 8
  %320 = fmul double %319, %274
  %321 = fmul double %320, 5.000000e-01
  %322 = fadd double %318, %321
  store double %322, double* %301, align 8
  %323 = load i32, i32* %62, align 4
  %324 = sext i32 %323 to i64
  %325 = getelementptr inbounds double, double* %tx, i64 %324
  %326 = load double, double* %325, align 8
  %327 = load double, double* %238, align 8
  %328 = fmul double %327, %266
  %329 = fmul double %328, 5.000000e-01
  %330 = fadd double %326, %329
  store double %330, double* %325, align 8
  %331 = load double, double* %243, align 8
  %332 = fmul double %331, %268
  %333 = fmul double %332, 5.000000e-01
  %334 = fadd double %330, %333
  store double %334, double* %325, align 8
  %335 = load double, double* %248, align 8
  %336 = fmul double %335, %270
  %337 = fmul double %336, 5.000000e-01
  %338 = fadd double %334, %337
  store double %338, double* %325, align 8
  %339 = load double, double* %253, align 8
  %340 = fmul double %339, %272
  %341 = fmul double %340, 5.000000e-01
  %342 = fadd double %338, %341
  store double %342, double* %325, align 8
  %343 = load double, double* %258, align 8
  %344 = fmul double %343, %274
  %345 = fmul double %344, 5.000000e-01
  %346 = fadd double %342, %345
  store double %346, double* %325, align 8
  %indvars.iv.next258 = add nuw nsw i64 %indvars.iv257, 1
  br label %.preheader11

347:                                              ; preds = %264
  %348 = load i32, i32* %263, align 4
  %349 = sext i32 %348 to i64
  %350 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 %349, i64 %indvars.iv245
  %351 = load i32, i32* %350, align 4
  %352 = sext i32 %351 to i64
  %353 = getelementptr inbounds double, double* %tx, i64 %352
  %354 = load double, double* %353, align 8
  %355 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 %349, i64 %indvars.iv245
  %356 = load double, double* %355, align 8
  %357 = fmul double %356, 5.000000e-01
  %358 = fadd double %354, %357
  store double %358, double* %353, align 8
  %359 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 0, i64 %indvars.iv245
  %360 = load double, double* %359, align 8
  %361 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 1, i64 %indvars.iv245
  %362 = load double, double* %361, align 8
  %363 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 2, i64 %indvars.iv245
  %364 = load double, double* %363, align 8
  %365 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 3, i64 %indvars.iv245
  %366 = load double, double* %365, align 8
  %367 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv257, i64 4, i64 %indvars.iv245
  %368 = load double, double* %367, align 8
  %369 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 %indvars.iv245
  %370 = load i32, i32* %369, align 4
  %371 = sext i32 %370 to i64
  %372 = getelementptr inbounds double, double* %tx, i64 %371
  %373 = load double, double* %372, align 8
  %374 = load double, double* %180, align 8
  %375 = fmul double %374, %360
  %376 = fadd double %373, %375
  store double %376, double* %372, align 8
  %377 = load double, double* %185, align 8
  %378 = fmul double %377, %362
  %379 = fadd double %376, %378
  store double %379, double* %372, align 8
  %380 = load double, double* %190, align 8
  %381 = fmul double %380, %364
  %382 = fadd double %379, %381
  store double %382, double* %372, align 8
  %383 = load double, double* %195, align 8
  %384 = fmul double %383, %366
  %385 = fadd double %382, %384
  store double %385, double* %372, align 8
  %386 = load double, double* %200, align 8
  %387 = fmul double %386, %368
  %388 = fadd double %385, %387
  store double %388, double* %372, align 8
  %389 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 2, i64 %indvars.iv245
  %390 = load i32, i32* %389, align 4
  %391 = sext i32 %390 to i64
  %392 = getelementptr inbounds double, double* %tx, i64 %391
  %393 = load double, double* %392, align 8
  %394 = load double, double* %209, align 8
  %395 = fmul double %394, %360
  %396 = fadd double %393, %395
  store double %396, double* %392, align 8
  %397 = load double, double* %214, align 8
  %398 = fmul double %397, %362
  %399 = fadd double %396, %398
  store double %399, double* %392, align 8
  %400 = load double, double* %219, align 8
  %401 = fmul double %400, %364
  %402 = fadd double %399, %401
  store double %402, double* %392, align 8
  %403 = load double, double* %224, align 8
  %404 = fmul double %403, %366
  %405 = fadd double %402, %404
  store double %405, double* %392, align 8
  %406 = load double, double* %229, align 8
  %407 = fmul double %406, %368
  %408 = fadd double %405, %407
  store double %408, double* %392, align 8
  %409 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 3, i64 %indvars.iv245
  %410 = load i32, i32* %409, align 4
  %411 = sext i32 %410 to i64
  %412 = getelementptr inbounds double, double* %tx, i64 %411
  %413 = load double, double* %412, align 8
  %414 = load double, double* %238, align 8
  %415 = fmul double %414, %360
  %416 = fadd double %413, %415
  store double %416, double* %412, align 8
  %417 = load double, double* %243, align 8
  %418 = fmul double %417, %362
  %419 = fadd double %416, %418
  store double %419, double* %412, align 8
  %420 = load double, double* %248, align 8
  %421 = fmul double %420, %364
  %422 = fadd double %419, %421
  store double %422, double* %412, align 8
  %423 = load double, double* %253, align 8
  %424 = fmul double %423, %366
  %425 = fadd double %422, %424
  store double %425, double* %412, align 8
  %426 = load double, double* %258, align 8
  %427 = fmul double %426, %368
  %428 = fadd double %425, %427
  store double %428, double* %412, align 8
  %indvars.iv.next246 = add nuw nsw i64 %indvars.iv245, 1
  br label %264

.preheader28.1:                                   ; preds = %7
  %429 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 1
  %430 = load i32, i32* %429, align 4
  %431 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 1, i64 1
  %432 = load i32, i32* %431, align 4
  %433 = sext i32 %432 to i64
  %434 = getelementptr inbounds double, double* %tmor, i64 %433
  %435 = bitcast double* %434 to i64*
  %436 = load i64, i64* %435, align 8
  %437 = sext i32 %430 to i64
  %438 = getelementptr inbounds double, double* %tx, i64 %437
  %439 = bitcast double* %438 to i64*
  store i64 %436, i64* %439, align 8
  %440 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 2
  %441 = load i32, i32* %440, align 4
  %442 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 1, i64 2
  %443 = load i32, i32* %442, align 4
  %444 = sext i32 %443 to i64
  %445 = getelementptr inbounds double, double* %tmor, i64 %444
  %446 = bitcast double* %445 to i64*
  %447 = load i64, i64* %446, align 8
  %448 = sext i32 %441 to i64
  %449 = getelementptr inbounds double, double* %tx, i64 %448
  %450 = bitcast double* %449 to i64*
  store i64 %447, i64* %450, align 8
  %451 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 3
  %452 = load i32, i32* %451, align 4
  %453 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 1, i64 3
  %454 = load i32, i32* %453, align 4
  %455 = sext i32 %454 to i64
  %456 = getelementptr inbounds double, double* %tmor, i64 %455
  %457 = bitcast double* %456 to i64*
  %458 = load i64, i64* %457, align 8
  %459 = sext i32 %452 to i64
  %460 = getelementptr inbounds double, double* %tx, i64 %459
  %461 = bitcast double* %460 to i64*
  store i64 %458, i64* %461, align 8
  %462 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 2, i64 1
  %463 = load i32, i32* %462, align 4
  %464 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 2, i64 1
  %465 = load i32, i32* %464, align 4
  %466 = sext i32 %465 to i64
  %467 = getelementptr inbounds double, double* %tmor, i64 %466
  %468 = bitcast double* %467 to i64*
  %469 = load i64, i64* %468, align 8
  %470 = sext i32 %463 to i64
  %471 = getelementptr inbounds double, double* %tx, i64 %470
  %472 = bitcast double* %471 to i64*
  store i64 %469, i64* %472, align 8
  %473 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 2, i64 2
  %474 = load i32, i32* %473, align 4
  %475 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 2, i64 2
  %476 = load i32, i32* %475, align 8
  %477 = sext i32 %476 to i64
  %478 = getelementptr inbounds double, double* %tmor, i64 %477
  %479 = bitcast double* %478 to i64*
  %480 = load i64, i64* %479, align 8
  %481 = sext i32 %474 to i64
  %482 = getelementptr inbounds double, double* %tx, i64 %481
  %483 = bitcast double* %482 to i64*
  store i64 %480, i64* %483, align 8
  %484 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 2, i64 3
  %485 = load i32, i32* %484, align 4
  %486 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 2, i64 3
  %487 = load i32, i32* %486, align 4
  %488 = sext i32 %487 to i64
  %489 = getelementptr inbounds double, double* %tmor, i64 %488
  %490 = bitcast double* %489 to i64*
  %491 = load i64, i64* %490, align 8
  %492 = sext i32 %485 to i64
  %493 = getelementptr inbounds double, double* %tx, i64 %492
  %494 = bitcast double* %493 to i64*
  store i64 %491, i64* %494, align 8
  %495 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 3, i64 1
  %496 = load i32, i32* %495, align 4
  %497 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 3, i64 1
  %498 = load i32, i32* %497, align 4
  %499 = sext i32 %498 to i64
  %500 = getelementptr inbounds double, double* %tmor, i64 %499
  %501 = bitcast double* %500 to i64*
  %502 = load i64, i64* %501, align 8
  %503 = sext i32 %496 to i64
  %504 = getelementptr inbounds double, double* %tx, i64 %503
  %505 = bitcast double* %504 to i64*
  store i64 %502, i64* %505, align 8
  %506 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 3, i64 2
  %507 = load i32, i32* %506, align 4
  %508 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 3, i64 2
  %509 = load i32, i32* %508, align 4
  %510 = sext i32 %509 to i64
  %511 = getelementptr inbounds double, double* %tmor, i64 %510
  %512 = bitcast double* %511 to i64*
  %513 = load i64, i64* %512, align 8
  %514 = sext i32 %507 to i64
  %515 = getelementptr inbounds double, double* %tx, i64 %514
  %516 = bitcast double* %515 to i64*
  store i64 %513, i64* %516, align 8
  %517 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 3, i64 3
  %518 = load i32, i32* %517, align 4
  %519 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 3, i64 3
  %520 = load i32, i32* %519, align 4
  %521 = sext i32 %520 to i64
  %522 = getelementptr inbounds double, double* %tmor, i64 %521
  %523 = bitcast double* %522 to i64*
  %524 = load i64, i64* %523, align 8
  %525 = sext i32 %518 to i64
  %526 = getelementptr inbounds double, double* %tx, i64 %525
  %527 = bitcast double* %526 to i64*
  store i64 %524, i64* %527, align 8
  %528 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 0, i64 4
  %529 = load i32, i32* %528, align 16
  %530 = icmp eq i32 %529, -1
  br i1 %530, label %.loopexit25.loopexit, label %.preheader26.preheader

.preheader26.preheader:                           ; preds = %.preheader28.1
  %531 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 0, i64 1
  %532 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 0, i64 2
  %533 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 0, i64 3
  %534 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 0, i64 0, i64 0
  %535 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 0, i64 0, i64 1
  %536 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 0, i64 0, i64 2
  %537 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 0, i64 0, i64 3
  br label %.preheader26

.preheader26:                                     ; preds = %538, %.preheader26.preheader
  %indvars.iv51 = phi i64 [ %indvars.iv.next52, %538 ], [ 1, %.preheader26.preheader ]
  %exitcond53 = icmp eq i64 %indvars.iv51, 4
  br i1 %exitcond53, label %.loopexit25, label %538

538:                                              ; preds = %.preheader26
  %539 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 %indvars.iv51
  %540 = load i32, i32* %539, align 4
  %541 = sext i32 %540 to i64
  %542 = getelementptr inbounds double, double* %tx, i64 %541
  %543 = add nsw i64 %indvars.iv51, -1
  %544 = load i32, i32* %16, align 16
  %545 = load double, double* %542, align 8
  %546 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %543
  %547 = load double, double* %546, align 8
  %548 = sext i32 %544 to i64
  %549 = getelementptr inbounds double, double* %tmor, i64 %548
  %550 = load double, double* %549, align 8
  %551 = fmul double %547, %550
  %552 = fmul double %551, 5.000000e-01
  %553 = fadd double %545, %552
  store double %553, double* %542, align 8
  %554 = load i32, i32* %531, align 4
  %555 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 %543
  %556 = load double, double* %555, align 8
  %557 = sext i32 %554 to i64
  %558 = getelementptr inbounds double, double* %tmor, i64 %557
  %559 = load double, double* %558, align 8
  %560 = fmul double %556, %559
  %561 = fmul double %560, 5.000000e-01
  %562 = fadd double %553, %561
  store double %562, double* %542, align 8
  %563 = load i32, i32* %532, align 8
  %564 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 %543
  %565 = load double, double* %564, align 8
  %566 = sext i32 %563 to i64
  %567 = getelementptr inbounds double, double* %tmor, i64 %566
  %568 = load double, double* %567, align 8
  %569 = fmul double %565, %568
  %570 = fmul double %569, 5.000000e-01
  %571 = fadd double %562, %570
  store double %571, double* %542, align 8
  %572 = load i32, i32* %533, align 4
  %573 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 %543
  %574 = load double, double* %573, align 8
  %575 = sext i32 %572 to i64
  %576 = getelementptr inbounds double, double* %tmor, i64 %575
  %577 = load double, double* %576, align 8
  %578 = fmul double %574, %577
  %579 = fmul double %578, 5.000000e-01
  %580 = fadd double %571, %579
  store double %580, double* %542, align 8
  %581 = load i32, i32* %528, align 16
  %582 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 %543
  %583 = load double, double* %582, align 8
  %584 = sext i32 %581 to i64
  %585 = getelementptr inbounds double, double* %tmor, i64 %584
  %586 = load double, double* %585, align 8
  %587 = fmul double %583, %586
  %588 = fmul double %587, 5.000000e-01
  %589 = fadd double %580, %588
  store double %589, double* %542, align 8
  %590 = load i32, i32* %534, align 8
  %591 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 0, i64 %543
  %592 = load double, double* %591, align 8
  %593 = sext i32 %590 to i64
  %594 = getelementptr inbounds double, double* %tmor, i64 %593
  %595 = load double, double* %594, align 8
  %596 = fmul double %592, %595
  %597 = fmul double %596, 5.000000e-01
  %598 = fadd double %589, %597
  store double %598, double* %542, align 8
  %599 = load i32, i32* %535, align 4
  %600 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 1, i64 %543
  %601 = load double, double* %600, align 8
  %602 = sext i32 %599 to i64
  %603 = getelementptr inbounds double, double* %tmor, i64 %602
  %604 = load double, double* %603, align 8
  %605 = fmul double %601, %604
  %606 = fmul double %605, 5.000000e-01
  %607 = fadd double %598, %606
  store double %607, double* %542, align 8
  %608 = load i32, i32* %536, align 8
  %609 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 2, i64 %543
  %610 = load double, double* %609, align 8
  %611 = sext i32 %608 to i64
  %612 = getelementptr inbounds double, double* %tmor, i64 %611
  %613 = load double, double* %612, align 8
  %614 = fmul double %610, %613
  %615 = fmul double %614, 5.000000e-01
  %616 = fadd double %607, %615
  store double %616, double* %542, align 8
  %617 = load i32, i32* %537, align 4
  %618 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 3, i64 %543
  %619 = load double, double* %618, align 8
  %620 = sext i32 %617 to i64
  %621 = getelementptr inbounds double, double* %tmor, i64 %620
  %622 = load double, double* %621, align 8
  %623 = fmul double %619, %622
  %624 = fmul double %623, 5.000000e-01
  %625 = fadd double %616, %624
  store double %625, double* %542, align 8
  %626 = load i32, i32* %18, align 8
  %627 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 4, i64 %543
  %628 = load double, double* %627, align 8
  %629 = sext i32 %626 to i64
  %630 = getelementptr inbounds double, double* %tmor, i64 %629
  %631 = load double, double* %630, align 8
  %632 = fmul double %628, %631
  %633 = fmul double %632, 5.000000e-01
  %634 = fadd double %625, %633
  store double %634, double* %542, align 8
  %indvars.iv.next52 = add nuw nsw i64 %indvars.iv51, 1
  br label %.preheader26

.loopexit25.loopexit:                             ; preds = %.preheader28.1
  %635 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 1
  %636 = load i32, i32* %635, align 4
  %637 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 0, i64 1
  %638 = load i32, i32* %637, align 4
  %639 = sext i32 %638 to i64
  %640 = getelementptr inbounds double, double* %tmor, i64 %639
  %641 = bitcast double* %640 to i64*
  %642 = load i64, i64* %641, align 8
  %643 = sext i32 %636 to i64
  %644 = getelementptr inbounds double, double* %tx, i64 %643
  %645 = bitcast double* %644 to i64*
  store i64 %642, i64* %645, align 8
  %646 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 2
  %647 = load i32, i32* %646, align 4
  %648 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 0, i64 2
  %649 = load i32, i32* %648, align 8
  %650 = sext i32 %649 to i64
  %651 = getelementptr inbounds double, double* %tmor, i64 %650
  %652 = bitcast double* %651 to i64*
  %653 = load i64, i64* %652, align 8
  %654 = sext i32 %647 to i64
  %655 = getelementptr inbounds double, double* %tx, i64 %654
  %656 = bitcast double* %655 to i64*
  store i64 %653, i64* %656, align 8
  %657 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 3
  %658 = load i32, i32* %657, align 4
  %659 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 0, i64 3
  %660 = load i32, i32* %659, align 4
  %661 = sext i32 %660 to i64
  %662 = getelementptr inbounds double, double* %tmor, i64 %661
  %663 = bitcast double* %662 to i64*
  %664 = load i64, i64* %663, align 8
  %665 = sext i32 %658 to i64
  %666 = getelementptr inbounds double, double* %tx, i64 %665
  %667 = bitcast double* %666 to i64*
  store i64 %664, i64* %667, align 8
  br label %.loopexit25

.loopexit25:                                      ; preds = %.loopexit25.loopexit, %.preheader26
  %668 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 0, i64 1, i64 4
  %669 = load i32, i32* %668, align 4
  %670 = icmp eq i32 %669, -1
  br i1 %670, label %.loopexit21.loopexit, label %.preheader22.preheader

.preheader22.preheader:                           ; preds = %.loopexit25
  %671 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 0, i64 2, i64 4
  %672 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 0, i64 3, i64 4
  %673 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 0, i64 4, i64 4
  %674 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 1, i64 0, i64 4
  %675 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 1, i64 1, i64 4
  %676 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 1, i64 2, i64 4
  %677 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 1, i64 3, i64 4
  br label %.preheader22

.preheader22:                                     ; preds = %678, %.preheader22.preheader
  %indvars.iv80 = phi i64 [ %indvars.iv.next81, %678 ], [ 1, %.preheader22.preheader ]
  %exitcond82 = icmp eq i64 %indvars.iv80, 4
  br i1 %exitcond82, label %.loopexit21, label %678

678:                                              ; preds = %.preheader22
  %679 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 %indvars.iv80, i64 4
  %680 = load i32, i32* %679, align 4
  %681 = sext i32 %680 to i64
  %682 = getelementptr inbounds double, double* %tx, i64 %681
  %683 = add nsw i64 %indvars.iv80, -1
  %684 = load i32, i32* %18, align 8
  %685 = load double, double* %682, align 8
  %686 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %683
  %687 = load double, double* %686, align 8
  %688 = sext i32 %684 to i64
  %689 = getelementptr inbounds double, double* %tmor, i64 %688
  %690 = load double, double* %689, align 8
  %691 = fmul double %687, %690
  %692 = fmul double %691, 5.000000e-01
  %693 = fadd double %685, %692
  store double %693, double* %682, align 8
  %694 = load i32, i32* %668, align 4
  %695 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 %683
  %696 = load double, double* %695, align 8
  %697 = sext i32 %694 to i64
  %698 = getelementptr inbounds double, double* %tmor, i64 %697
  %699 = load double, double* %698, align 8
  %700 = fmul double %696, %699
  %701 = fmul double %700, 5.000000e-01
  %702 = fadd double %693, %701
  store double %702, double* %682, align 8
  %703 = load i32, i32* %671, align 8
  %704 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 %683
  %705 = load double, double* %704, align 8
  %706 = sext i32 %703 to i64
  %707 = getelementptr inbounds double, double* %tmor, i64 %706
  %708 = load double, double* %707, align 8
  %709 = fmul double %705, %708
  %710 = fmul double %709, 5.000000e-01
  %711 = fadd double %702, %710
  store double %711, double* %682, align 8
  %712 = load i32, i32* %672, align 4
  %713 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 %683
  %714 = load double, double* %713, align 8
  %715 = sext i32 %712 to i64
  %716 = getelementptr inbounds double, double* %tmor, i64 %715
  %717 = load double, double* %716, align 8
  %718 = fmul double %714, %717
  %719 = fmul double %718, 5.000000e-01
  %720 = fadd double %711, %719
  store double %720, double* %682, align 8
  %721 = load i32, i32* %673, align 8
  %722 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 %683
  %723 = load double, double* %722, align 8
  %724 = sext i32 %721 to i64
  %725 = getelementptr inbounds double, double* %tmor, i64 %724
  %726 = load double, double* %725, align 8
  %727 = fmul double %723, %726
  %728 = fmul double %727, 5.000000e-01
  %729 = fadd double %720, %728
  store double %729, double* %682, align 8
  %730 = load i32, i32* %674, align 4
  %731 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 0, i64 %683
  %732 = load double, double* %731, align 8
  %733 = sext i32 %730 to i64
  %734 = getelementptr inbounds double, double* %tmor, i64 %733
  %735 = load double, double* %734, align 8
  %736 = fmul double %732, %735
  %737 = fmul double %736, 5.000000e-01
  %738 = fadd double %729, %737
  store double %738, double* %682, align 8
  %739 = load i32, i32* %675, align 4
  %740 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 1, i64 %683
  %741 = load double, double* %740, align 8
  %742 = sext i32 %739 to i64
  %743 = getelementptr inbounds double, double* %tmor, i64 %742
  %744 = load double, double* %743, align 8
  %745 = fmul double %741, %744
  %746 = fmul double %745, 5.000000e-01
  %747 = fadd double %738, %746
  store double %747, double* %682, align 8
  %748 = load i32, i32* %676, align 4
  %749 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 2, i64 %683
  %750 = load double, double* %749, align 8
  %751 = sext i32 %748 to i64
  %752 = getelementptr inbounds double, double* %tmor, i64 %751
  %753 = load double, double* %752, align 8
  %754 = fmul double %750, %753
  %755 = fmul double %754, 5.000000e-01
  %756 = fadd double %747, %755
  store double %756, double* %682, align 8
  %757 = load i32, i32* %677, align 4
  %758 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 3, i64 %683
  %759 = load double, double* %758, align 8
  %760 = sext i32 %757 to i64
  %761 = getelementptr inbounds double, double* %tmor, i64 %760
  %762 = load double, double* %761, align 8
  %763 = fmul double %759, %762
  %764 = fmul double %763, 5.000000e-01
  %765 = fadd double %756, %764
  store double %765, double* %682, align 8
  %766 = load i32, i32* %22, align 4
  %767 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 4, i64 %683
  %768 = load double, double* %767, align 8
  %769 = sext i32 %766 to i64
  %770 = getelementptr inbounds double, double* %tmor, i64 %769
  %771 = load double, double* %770, align 8
  %772 = fmul double %768, %771
  %773 = fmul double %772, 5.000000e-01
  %774 = fadd double %765, %773
  store double %774, double* %682, align 8
  %indvars.iv.next81 = add nuw nsw i64 %indvars.iv80, 1
  br label %.preheader22

.loopexit21.loopexit:                             ; preds = %.loopexit25
  %775 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 4
  %776 = load i32, i32* %775, align 4
  %777 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 1, i64 4
  %778 = load i32, i32* %777, align 4
  %779 = sext i32 %778 to i64
  %780 = getelementptr inbounds double, double* %tmor, i64 %779
  %781 = bitcast double* %780 to i64*
  %782 = load i64, i64* %781, align 8
  %783 = sext i32 %776 to i64
  %784 = getelementptr inbounds double, double* %tx, i64 %783
  %785 = bitcast double* %784 to i64*
  store i64 %782, i64* %785, align 8
  %786 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 2, i64 4
  %787 = load i32, i32* %786, align 4
  %788 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 2, i64 4
  %789 = load i32, i32* %788, align 8
  %790 = sext i32 %789 to i64
  %791 = getelementptr inbounds double, double* %tmor, i64 %790
  %792 = bitcast double* %791 to i64*
  %793 = load i64, i64* %792, align 8
  %794 = sext i32 %787 to i64
  %795 = getelementptr inbounds double, double* %tx, i64 %794
  %796 = bitcast double* %795 to i64*
  store i64 %793, i64* %796, align 8
  %797 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 3, i64 4
  %798 = load i32, i32* %797, align 4
  %799 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 3, i64 4
  %800 = load i32, i32* %799, align 4
  %801 = sext i32 %800 to i64
  %802 = getelementptr inbounds double, double* %tmor, i64 %801
  %803 = bitcast double* %802 to i64*
  %804 = load i64, i64* %803, align 8
  %805 = sext i32 %798 to i64
  %806 = getelementptr inbounds double, double* %tx, i64 %805
  %807 = bitcast double* %806 to i64*
  store i64 %804, i64* %807, align 8
  br label %.loopexit21

.loopexit21:                                      ; preds = %.loopexit21.loopexit, %.preheader22
  %808 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 1, i64 4, i64 1
  %809 = load i32, i32* %808, align 4
  %810 = icmp eq i32 %809, -1
  br i1 %810, label %.loopexit17.loopexit, label %.preheader18.preheader

.preheader18.preheader:                           ; preds = %.loopexit21
  %811 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 1, i64 4, i64 2
  %812 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 1, i64 4, i64 3
  %813 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 1, i64 4, i64 4
  %814 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 1, i64 4, i64 0
  %815 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 1, i64 4, i64 1
  %816 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 1, i64 4, i64 2
  %817 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 1, i64 4, i64 3
  br label %.preheader18

.preheader18:                                     ; preds = %818, %.preheader18.preheader
  %indvars.iv117 = phi i64 [ %indvars.iv.next118, %818 ], [ 1, %.preheader18.preheader ]
  %exitcond119 = icmp eq i64 %indvars.iv117, 4
  br i1 %exitcond119, label %.loopexit17, label %818

818:                                              ; preds = %.preheader18
  %819 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 4, i64 %indvars.iv117
  %820 = load i32, i32* %819, align 4
  %821 = sext i32 %820 to i64
  %822 = getelementptr inbounds double, double* %tx, i64 %821
  %823 = add nsw i64 %indvars.iv117, -1
  %824 = load i32, i32* %20, align 4
  %825 = load double, double* %822, align 8
  %826 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %823
  %827 = load double, double* %826, align 8
  %828 = sext i32 %824 to i64
  %829 = getelementptr inbounds double, double* %tmor, i64 %828
  %830 = load double, double* %829, align 8
  %831 = fmul double %827, %830
  %832 = fmul double %831, 5.000000e-01
  %833 = fadd double %825, %832
  store double %833, double* %822, align 8
  %834 = load i32, i32* %808, align 4
  %835 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 %823
  %836 = load double, double* %835, align 8
  %837 = sext i32 %834 to i64
  %838 = getelementptr inbounds double, double* %tmor, i64 %837
  %839 = load double, double* %838, align 8
  %840 = fmul double %836, %839
  %841 = fmul double %840, 5.000000e-01
  %842 = fadd double %833, %841
  store double %842, double* %822, align 8
  %843 = load i32, i32* %811, align 4
  %844 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 %823
  %845 = load double, double* %844, align 8
  %846 = sext i32 %843 to i64
  %847 = getelementptr inbounds double, double* %tmor, i64 %846
  %848 = load double, double* %847, align 8
  %849 = fmul double %845, %848
  %850 = fmul double %849, 5.000000e-01
  %851 = fadd double %842, %850
  store double %851, double* %822, align 8
  %852 = load i32, i32* %812, align 4
  %853 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 %823
  %854 = load double, double* %853, align 8
  %855 = sext i32 %852 to i64
  %856 = getelementptr inbounds double, double* %tmor, i64 %855
  %857 = load double, double* %856, align 8
  %858 = fmul double %854, %857
  %859 = fmul double %858, 5.000000e-01
  %860 = fadd double %851, %859
  store double %860, double* %822, align 8
  %861 = load i32, i32* %813, align 4
  %862 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 %823
  %863 = load double, double* %862, align 8
  %864 = sext i32 %861 to i64
  %865 = getelementptr inbounds double, double* %tmor, i64 %864
  %866 = load double, double* %865, align 8
  %867 = fmul double %863, %866
  %868 = fmul double %867, 5.000000e-01
  %869 = fadd double %860, %868
  store double %869, double* %822, align 8
  %870 = load i32, i32* %814, align 4
  %871 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 0, i64 %823
  %872 = load double, double* %871, align 8
  %873 = sext i32 %870 to i64
  %874 = getelementptr inbounds double, double* %tmor, i64 %873
  %875 = load double, double* %874, align 8
  %876 = fmul double %872, %875
  %877 = fmul double %876, 5.000000e-01
  %878 = fadd double %869, %877
  store double %878, double* %822, align 8
  %879 = load i32, i32* %815, align 4
  %880 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 1, i64 %823
  %881 = load double, double* %880, align 8
  %882 = sext i32 %879 to i64
  %883 = getelementptr inbounds double, double* %tmor, i64 %882
  %884 = load double, double* %883, align 8
  %885 = fmul double %881, %884
  %886 = fmul double %885, 5.000000e-01
  %887 = fadd double %878, %886
  store double %887, double* %822, align 8
  %888 = load i32, i32* %816, align 4
  %889 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 2, i64 %823
  %890 = load double, double* %889, align 8
  %891 = sext i32 %888 to i64
  %892 = getelementptr inbounds double, double* %tmor, i64 %891
  %893 = load double, double* %892, align 8
  %894 = fmul double %890, %893
  %895 = fmul double %894, 5.000000e-01
  %896 = fadd double %887, %895
  store double %896, double* %822, align 8
  %897 = load i32, i32* %817, align 4
  %898 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 3, i64 %823
  %899 = load double, double* %898, align 8
  %900 = sext i32 %897 to i64
  %901 = getelementptr inbounds double, double* %tmor, i64 %900
  %902 = load double, double* %901, align 8
  %903 = fmul double %899, %902
  %904 = fmul double %903, 5.000000e-01
  %905 = fadd double %896, %904
  store double %905, double* %822, align 8
  %906 = load i32, i32* %22, align 4
  %907 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 4, i64 %823
  %908 = load double, double* %907, align 8
  %909 = sext i32 %906 to i64
  %910 = getelementptr inbounds double, double* %tmor, i64 %909
  %911 = load double, double* %910, align 8
  %912 = fmul double %908, %911
  %913 = fmul double %912, 5.000000e-01
  %914 = fadd double %905, %913
  store double %914, double* %822, align 8
  %indvars.iv.next118 = add nuw nsw i64 %indvars.iv117, 1
  br label %.preheader18

.loopexit17.loopexit:                             ; preds = %.loopexit21
  %915 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 4, i64 1
  %916 = load i32, i32* %915, align 4
  %917 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 4, i64 1
  %918 = load i32, i32* %917, align 4
  %919 = sext i32 %918 to i64
  %920 = getelementptr inbounds double, double* %tmor, i64 %919
  %921 = bitcast double* %920 to i64*
  %922 = load i64, i64* %921, align 8
  %923 = sext i32 %916 to i64
  %924 = getelementptr inbounds double, double* %tx, i64 %923
  %925 = bitcast double* %924 to i64*
  store i64 %922, i64* %925, align 8
  %926 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 4, i64 2
  %927 = load i32, i32* %926, align 4
  %928 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 4, i64 2
  %929 = load i32, i32* %928, align 8
  %930 = sext i32 %929 to i64
  %931 = getelementptr inbounds double, double* %tmor, i64 %930
  %932 = bitcast double* %931 to i64*
  %933 = load i64, i64* %932, align 8
  %934 = sext i32 %927 to i64
  %935 = getelementptr inbounds double, double* %tx, i64 %934
  %936 = bitcast double* %935 to i64*
  store i64 %933, i64* %936, align 8
  %937 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 4, i64 3
  %938 = load i32, i32* %937, align 4
  %939 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 4, i64 3
  %940 = load i32, i32* %939, align 4
  %941 = sext i32 %940 to i64
  %942 = getelementptr inbounds double, double* %tmor, i64 %941
  %943 = bitcast double* %942 to i64*
  %944 = load i64, i64* %943, align 8
  %945 = sext i32 %938 to i64
  %946 = getelementptr inbounds double, double* %tx, i64 %945
  %947 = bitcast double* %946 to i64*
  store i64 %944, i64* %947, align 8
  br label %.loopexit17

.loopexit17:                                      ; preds = %.loopexit17.loopexit, %.preheader18
  %948 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 4, i64 0
  %949 = load i32, i32* %948, align 16
  %950 = icmp eq i32 %949, -1
  br i1 %950, label %.loopexit.loopexit30, label %.preheader14.preheader

.preheader14.preheader:                           ; preds = %.loopexit17
  %951 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 1, i64 0
  %952 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 2, i64 0
  %953 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 3, i64 0
  %954 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 1, i64 0, i64 0
  %955 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 1, i64 1, i64 0
  %956 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 1, i64 2, i64 0
  %957 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 1, i64 3, i64 0
  br label %.preheader14

.preheader14:                                     ; preds = %958, %.preheader14.preheader
  %indvars.iv162 = phi i64 [ %indvars.iv.next163, %958 ], [ 1, %.preheader14.preheader ]
  %exitcond164 = icmp eq i64 %indvars.iv162, 4
  br i1 %exitcond164, label %.loopexit, label %958

958:                                              ; preds = %.preheader14
  %959 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 %indvars.iv162, i64 0
  %960 = load i32, i32* %959, align 4
  %961 = sext i32 %960 to i64
  %962 = getelementptr inbounds double, double* %tx, i64 %961
  %963 = add nsw i64 %indvars.iv162, -1
  %964 = load i32, i32* %16, align 16
  %965 = load double, double* %962, align 8
  %966 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %963
  %967 = load double, double* %966, align 8
  %968 = sext i32 %964 to i64
  %969 = getelementptr inbounds double, double* %tmor, i64 %968
  %970 = load double, double* %969, align 8
  %971 = fmul double %967, %970
  %972 = fmul double %971, 5.000000e-01
  %973 = fadd double %965, %972
  store double %973, double* %962, align 8
  %974 = load i32, i32* %951, align 4
  %975 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 %963
  %976 = load double, double* %975, align 8
  %977 = sext i32 %974 to i64
  %978 = getelementptr inbounds double, double* %tmor, i64 %977
  %979 = load double, double* %978, align 8
  %980 = fmul double %976, %979
  %981 = fmul double %980, 5.000000e-01
  %982 = fadd double %973, %981
  store double %982, double* %962, align 8
  %983 = load i32, i32* %952, align 8
  %984 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 %963
  %985 = load double, double* %984, align 8
  %986 = sext i32 %983 to i64
  %987 = getelementptr inbounds double, double* %tmor, i64 %986
  %988 = load double, double* %987, align 8
  %989 = fmul double %985, %988
  %990 = fmul double %989, 5.000000e-01
  %991 = fadd double %982, %990
  store double %991, double* %962, align 8
  %992 = load i32, i32* %953, align 4
  %993 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 %963
  %994 = load double, double* %993, align 8
  %995 = sext i32 %992 to i64
  %996 = getelementptr inbounds double, double* %tmor, i64 %995
  %997 = load double, double* %996, align 8
  %998 = fmul double %994, %997
  %999 = fmul double %998, 5.000000e-01
  %1000 = fadd double %991, %999
  store double %1000, double* %962, align 8
  %1001 = load i32, i32* %948, align 16
  %1002 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 %963
  %1003 = load double, double* %1002, align 8
  %1004 = sext i32 %1001 to i64
  %1005 = getelementptr inbounds double, double* %tmor, i64 %1004
  %1006 = load double, double* %1005, align 8
  %1007 = fmul double %1003, %1006
  %1008 = fmul double %1007, 5.000000e-01
  %1009 = fadd double %1000, %1008
  store double %1009, double* %962, align 8
  %1010 = load i32, i32* %954, align 4
  %1011 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 0, i64 %963
  %1012 = load double, double* %1011, align 8
  %1013 = sext i32 %1010 to i64
  %1014 = getelementptr inbounds double, double* %tmor, i64 %1013
  %1015 = load double, double* %1014, align 8
  %1016 = fmul double %1012, %1015
  %1017 = fmul double %1016, 5.000000e-01
  %1018 = fadd double %1009, %1017
  store double %1018, double* %962, align 8
  %1019 = load i32, i32* %955, align 4
  %1020 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 1, i64 %963
  %1021 = load double, double* %1020, align 8
  %1022 = sext i32 %1019 to i64
  %1023 = getelementptr inbounds double, double* %tmor, i64 %1022
  %1024 = load double, double* %1023, align 8
  %1025 = fmul double %1021, %1024
  %1026 = fmul double %1025, 5.000000e-01
  %1027 = fadd double %1018, %1026
  store double %1027, double* %962, align 8
  %1028 = load i32, i32* %956, align 4
  %1029 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 2, i64 %963
  %1030 = load double, double* %1029, align 8
  %1031 = sext i32 %1028 to i64
  %1032 = getelementptr inbounds double, double* %tmor, i64 %1031
  %1033 = load double, double* %1032, align 8
  %1034 = fmul double %1030, %1033
  %1035 = fmul double %1034, 5.000000e-01
  %1036 = fadd double %1027, %1035
  store double %1036, double* %962, align 8
  %1037 = load i32, i32* %957, align 4
  %1038 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 3, i64 %963
  %1039 = load double, double* %1038, align 8
  %1040 = sext i32 %1037 to i64
  %1041 = getelementptr inbounds double, double* %tmor, i64 %1040
  %1042 = load double, double* %1041, align 8
  %1043 = fmul double %1039, %1042
  %1044 = fmul double %1043, 5.000000e-01
  %1045 = fadd double %1036, %1044
  store double %1045, double* %962, align 8
  %1046 = load i32, i32* %20, align 4
  %1047 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 4, i64 %963
  %1048 = load double, double* %1047, align 8
  %1049 = sext i32 %1046 to i64
  %1050 = getelementptr inbounds double, double* %tmor, i64 %1049
  %1051 = load double, double* %1050, align 8
  %1052 = fmul double %1048, %1051
  %1053 = fmul double %1052, 5.000000e-01
  %1054 = fadd double %1045, %1053
  store double %1054, double* %962, align 8
  %indvars.iv.next163 = add nuw nsw i64 %indvars.iv162, 1
  br label %.preheader14

.loopexit.loopexit30:                             ; preds = %.loopexit17
  %1055 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 1, i64 0
  %1056 = load i32, i32* %1055, align 4
  %1057 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 1, i64 0
  %1058 = load i32, i32* %1057, align 4
  %1059 = sext i32 %1058 to i64
  %1060 = getelementptr inbounds double, double* %tmor, i64 %1059
  %1061 = bitcast double* %1060 to i64*
  %1062 = load i64, i64* %1061, align 8
  %1063 = sext i32 %1056 to i64
  %1064 = getelementptr inbounds double, double* %tx, i64 %1063
  %1065 = bitcast double* %1064 to i64*
  store i64 %1062, i64* %1065, align 8
  %1066 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 2, i64 0
  %1067 = load i32, i32* %1066, align 4
  %1068 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 2, i64 0
  %1069 = load i32, i32* %1068, align 8
  %1070 = sext i32 %1069 to i64
  %1071 = getelementptr inbounds double, double* %tmor, i64 %1070
  %1072 = bitcast double* %1071 to i64*
  %1073 = load i64, i64* %1072, align 8
  %1074 = sext i32 %1067 to i64
  %1075 = getelementptr inbounds double, double* %tx, i64 %1074
  %1076 = bitcast double* %1075 to i64*
  store i64 %1073, i64* %1076, align 8
  %1077 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 3, i64 0
  %1078 = load i32, i32* %1077, align 4
  %1079 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv264, i64 %indvars.iv261, i64 0, i64 0, i64 3, i64 0
  %1080 = load i32, i32* %1079, align 4
  %1081 = sext i32 %1080 to i64
  %1082 = getelementptr inbounds double, double* %tmor, i64 %1081
  %1083 = bitcast double* %1082 to i64*
  %1084 = load i64, i64* %1083, align 8
  %1085 = sext i32 %1078 to i64
  %1086 = getelementptr inbounds double, double* %tx, i64 %1085
  %1087 = bitcast double* %1086 to i64*
  store i64 %1084, i64* %1087, align 8
  br label %.loopexit

.loopexit:                                        ; preds = %.loopexit.loopexit30, %.preheader14, %.preheader11
  %indvars.iv.next262 = add nuw nsw i64 %indvars.iv261, 1
  br label %.preheader29

1088:                                             ; preds = %.preheader29
  %indvars.iv.next265 = add nuw nsw i64 %indvars.iv264, 1
  br label %3

1089:                                             ; preds = %3
  ret void
}

declare void @col2(double*, double*, i32) local_unnamed_addr #1

declare void @r_init(double*, i32, double) local_unnamed_addr #1

; Function Attrs: nounwind uwtable
define void @transfb(double* %tmor, double* nocapture readonly %tx) local_unnamed_addr #0 {
  %temp = alloca [2 x [5 x [5 x double]]], align 16
  %top = alloca [2 x [5 x double]], align 16
  %1 = load i32, i32* @nmor, align 4
  tail call void @r_init(double* %tmor, i32 %1, double 0.000000e+00) #4
  %2 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 0, i64 0, i64 0
  br label %3

3:                                                ; preds = %803, %0
  %indvars.iv284 = phi i64 [ %indvars.iv.next285, %803 ], [ 0, %0 ]
  %4 = load i32, i32* @nelt, align 4
  %5 = sext i32 %4 to i64
  %6 = icmp slt i64 %indvars.iv284, %5
  br i1 %6, label %.preheader32, label %804

.preheader32:                                     ; preds = %.loopexit, %3
  %indvars.iv281 = phi i64 [ %indvars.iv.next282, %.loopexit ], [ 0, %3 ]
  %exitcond283 = icmp eq i64 %indvars.iv281, 6
  br i1 %exitcond283, label %803, label %7

7:                                                ; preds = %.preheader32
  %8 = getelementptr inbounds [8800 x [6 x i32]], [8800 x [6 x i32]]* @cbc, i64 0, i64 %indvars.iv284, i64 %indvars.iv281
  %9 = load i32, i32* %8, align 4
  %10 = icmp eq i32 %9, 3
  %11 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0
  %12 = load i32, i32* %11, align 4
  %13 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 4
  %14 = load i32, i32* %13, align 4
  %15 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 4, i64 0
  %16 = load i32, i32* %15, align 4
  %17 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 4, i64 4
  %18 = load i32, i32* %17, align 4
  %19 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 0, i64 0
  %20 = load i32, i32* %19, align 16
  %21 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 1, i64 0, i64 0, i64 4
  %22 = load i32, i32* %21, align 8
  %23 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 1, i64 4, i64 0
  %24 = load i32, i32* %23, align 4
  %25 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 1, i64 1, i64 4, i64 4
  %26 = load i32, i32* %25, align 4
  %27 = sext i32 %20 to i64
  %28 = getelementptr inbounds double, double* %tmor, i64 %27
  %29 = load double, double* %28, align 8
  %30 = sext i32 %12 to i64
  %31 = getelementptr inbounds double, double* %tx, i64 %30
  %32 = load double, double* %31, align 8
  %33 = fmul double %32, 0x3FD5555555555555
  %34 = fadd double %29, %33
  store double %34, double* %28, align 8
  %35 = sext i32 %22 to i64
  %36 = getelementptr inbounds double, double* %tmor, i64 %35
  %37 = load double, double* %36, align 8
  %38 = sext i32 %14 to i64
  %39 = getelementptr inbounds double, double* %tx, i64 %38
  %40 = load double, double* %39, align 8
  %41 = fmul double %40, 0x3FD5555555555555
  %42 = fadd double %37, %41
  store double %42, double* %36, align 8
  %43 = sext i32 %24 to i64
  %44 = getelementptr inbounds double, double* %tmor, i64 %43
  %45 = load double, double* %44, align 8
  %46 = sext i32 %16 to i64
  %47 = getelementptr inbounds double, double* %tx, i64 %46
  %48 = load double, double* %47, align 8
  %49 = fmul double %48, 0x3FD5555555555555
  %50 = fadd double %45, %49
  store double %50, double* %44, align 8
  %51 = sext i32 %26 to i64
  %52 = getelementptr inbounds double, double* %tmor, i64 %51
  %53 = load double, double* %52, align 8
  %54 = sext i32 %18 to i64
  %55 = getelementptr inbounds double, double* %tx, i64 %54
  %56 = load double, double* %55, align 8
  %57 = fmul double %56, 0x3FD5555555555555
  %58 = fadd double %53, %57
  store double %58, double* %52, align 8
  br i1 %10, label %59, label %.preheader31.1

59:                                               ; preds = %7
  call void @r_init(double* nonnull %2, i32 50, double 0.000000e+00) #4
  br label %60

60:                                               ; preds = %161, %59
  %indvars.iv241 = phi i64 [ %indvars.iv.next242, %161 ], [ 0, %59 ]
  %indvars.iv239 = phi i64 [ %indvars.iv.next240, %161 ], [ 5, %59 ]
  %indvars.iv229 = phi i64 [ %indvars.iv.next230, %161 ], [ 1, %59 ]
  %exitcond244 = icmp eq i64 %indvars.iv241, 2
  br i1 %exitcond244, label %.preheader14, label %.preheader8

.preheader8:                                      ; preds = %60
  %61 = getelementptr inbounds [2 x i32], [2 x i32]* @v_end, i64 0, i64 %indvars.iv241
  %62 = load i32, i32* %61, align 4
  %63 = sext i32 %62 to i64
  %64 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %63, i64 0
  %65 = load double, double* %64, align 8
  %66 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %63, i64 1
  %67 = load double, double* %66, align 8
  %68 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %63, i64 2
  %69 = load double, double* %68, align 8
  %70 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %indvars.iv229, i64 0
  %71 = load double, double* %70, align 8
  %72 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %indvars.iv229, i64 1
  %73 = load double, double* %72, align 8
  %74 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %indvars.iv229, i64 2
  %75 = load double, double* %74, align 8
  %indvars.iv.next232 = add nsw i64 %indvars.iv229, 1
  %76 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %indvars.iv.next232, i64 0
  %77 = load double, double* %76, align 8
  %78 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %indvars.iv.next232, i64 1
  %79 = load double, double* %78, align 8
  %80 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %indvars.iv.next232, i64 2
  %81 = load double, double* %80, align 8
  %indvars.iv.next232.1 = add nsw i64 %indvars.iv229, 2
  %82 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %indvars.iv.next232.1, i64 0
  %83 = load double, double* %82, align 8
  %84 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %indvars.iv.next232.1, i64 1
  %85 = load double, double* %84, align 8
  %86 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %indvars.iv.next232.1, i64 2
  %87 = load double, double* %86, align 8
  %indvars.iv.next232.2 = add nsw i64 %indvars.iv229, 3
  %88 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %indvars.iv.next232.2, i64 0
  %89 = load double, double* %88, align 8
  %90 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %indvars.iv.next232.2, i64 1
  %91 = load double, double* %90, align 8
  %92 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv241, i64 %indvars.iv.next232.2, i64 2
  %93 = load double, double* %92, align 8
  %indvars.iv.next232.3 = add nsw i64 %indvars.iv229, 4
  %exitcond235.4 = icmp eq i64 %indvars.iv.next232.3, %indvars.iv239
  br label %94

94:                                               ; preds = %.preheader2, %.preheader8
  %indvars.iv236 = phi i64 [ 0, %.preheader8 ], [ %indvars.iv.next237, %.preheader2 ]
  %exitcond238 = icmp eq i64 %indvars.iv236, 5
  br i1 %exitcond238, label %161, label %.preheader2

.preheader2:                                      ; preds = %94
  %95 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 %63, i64 %indvars.iv236
  %96 = load i32, i32* %95, align 4
  %97 = sext i32 %96 to i64
  %98 = getelementptr inbounds double, double* %tx, i64 %97
  %99 = bitcast double* %98 to i64*
  %100 = load i64, i64* %99, align 8
  %101 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv241, i64 %63, i64 %indvars.iv236
  %102 = bitcast double* %101 to i64*
  store i64 %100, i64* %102, align 8
  %103 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 1, i64 %indvars.iv236
  %104 = load i32, i32* %103, align 4
  %105 = sext i32 %104 to i64
  %106 = getelementptr inbounds double, double* %tx, i64 %105
  %107 = load double, double* %106, align 8
  %108 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 2, i64 %indvars.iv236
  %109 = load i32, i32* %108, align 4
  %110 = sext i32 %109 to i64
  %111 = getelementptr inbounds double, double* %tx, i64 %110
  %112 = load double, double* %111, align 8
  %113 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 3, i64 %indvars.iv236
  %114 = load i32, i32* %113, align 4
  %115 = sext i32 %114 to i64
  %116 = getelementptr inbounds double, double* %tx, i64 %115
  %117 = load double, double* %116, align 8
  %118 = fmul double %65, %107
  %119 = fadd double %118, 0.000000e+00
  %120 = fmul double %67, %112
  %121 = fadd double %119, %120
  %122 = fmul double %69, %117
  %123 = fadd double %121, %122
  %124 = getelementptr inbounds [2 x [5 x double]], [2 x [5 x double]]* %top, i64 0, i64 %indvars.iv241, i64 %indvars.iv236
  store double %123, double* %124, align 8
  %125 = fmul double %71, %107
  %126 = fadd double %125, 0.000000e+00
  %127 = fmul double %73, %112
  %128 = fadd double %126, %127
  %129 = fmul double %75, %117
  %130 = fadd double %128, %129
  %131 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv241, i64 %indvars.iv229, i64 %indvars.iv236
  %132 = load double, double* %131, align 8
  %133 = fadd double %130, %132
  store double %133, double* %131, align 8
  %134 = fmul double %77, %107
  %135 = fadd double %134, 0.000000e+00
  %136 = fmul double %79, %112
  %137 = fadd double %135, %136
  %138 = fmul double %81, %117
  %139 = fadd double %137, %138
  %140 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv241, i64 %indvars.iv.next232, i64 %indvars.iv236
  %141 = load double, double* %140, align 8
  %142 = fadd double %139, %141
  store double %142, double* %140, align 8
  %143 = fmul double %83, %107
  %144 = fadd double %143, 0.000000e+00
  %145 = fmul double %85, %112
  %146 = fadd double %144, %145
  %147 = fmul double %87, %117
  %148 = fadd double %146, %147
  %149 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv241, i64 %indvars.iv.next232.1, i64 %indvars.iv236
  %150 = load double, double* %149, align 8
  %151 = fadd double %148, %150
  store double %151, double* %149, align 8
  %152 = fmul double %89, %107
  %153 = fadd double %152, 0.000000e+00
  %154 = fmul double %91, %112
  %155 = fadd double %153, %154
  %156 = fmul double %93, %117
  %157 = fadd double %155, %156
  %158 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv241, i64 %indvars.iv.next232.2, i64 %indvars.iv236
  %159 = load double, double* %158, align 8
  %160 = fadd double %157, %159
  store double %160, double* %158, align 8
  call void @llvm.assume(i1 %exitcond235.4)
  %indvars.iv.next237 = add nuw nsw i64 %indvars.iv236, 1
  br label %94

161:                                              ; preds = %94
  %indvars.iv.next242 = add nuw nsw i64 %indvars.iv241, 1
  %indvars.iv.next230 = add nsw i64 %indvars.iv229, -1
  %indvars.iv.next240 = add nsw i64 %indvars.iv239, -1
  br label %60

.preheader14:                                     ; preds = %415, %60
  %indvars.iv277 = phi i64 [ %indvars.iv.next278, %415 ], [ 0, %60 ]
  %indvars.iv275 = phi i64 [ %indvars.iv.next276, %415 ], [ 5, %60 ]
  %indvars.iv254 = phi i64 [ %indvars.iv.next255, %415 ], [ 1, %60 ]
  %exitcond280 = icmp eq i64 %indvars.iv277, 2
  br i1 %exitcond280, label %.loopexit, label %.preheader7

.preheader7:                                      ; preds = %.preheader14
  %162 = getelementptr inbounds [2 x i32], [2 x i32]* @v_end, i64 0, i64 %indvars.iv277
  %163 = getelementptr inbounds [2 x [5 x double]], [2 x [5 x double]]* %top, i64 0, i64 %indvars.iv277, i64 1
  %164 = load double, double* %163, align 8
  %165 = getelementptr inbounds [2 x [5 x double]], [2 x [5 x double]]* %top, i64 0, i64 %indvars.iv277, i64 2
  %166 = load double, double* %165, align 8
  %167 = getelementptr inbounds [2 x [5 x double]], [2 x [5 x double]]* %top, i64 0, i64 %indvars.iv277, i64 3
  %168 = load double, double* %167, align 8
  br label %169

169:                                              ; preds = %280, %.preheader7
  %indvars.iv271 = phi i64 [ 0, %.preheader7 ], [ %indvars.iv.next272, %280 ]
  %exitcond274 = icmp eq i64 %indvars.iv271, 2
  br i1 %exitcond274, label %415, label %170

170:                                              ; preds = %169
  %171 = getelementptr inbounds [2 x i32], [2 x i32]* @v_end, i64 0, i64 %indvars.iv271
  %172 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 0, i64 0
  %173 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 0, i64 1
  %174 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 0, i64 2
  %175 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 1, i64 0
  %176 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 1, i64 1
  %177 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 1, i64 2
  %178 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 2, i64 0
  %179 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 2, i64 1
  %180 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 2, i64 2
  %181 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 3, i64 0
  %182 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 3, i64 1
  %183 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 3, i64 2
  %184 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 4, i64 0
  %185 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 4, i64 1
  %186 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv271, i64 4, i64 2
  br label %187

187:                                              ; preds = %.preheader, %170
  %indvars.iv256 = phi i64 [ %indvars.iv.next257, %.preheader ], [ %indvars.iv254, %170 ]
  %exitcond260 = icmp eq i64 %indvars.iv256, %indvars.iv275
  br i1 %exitcond260, label %280, label %.preheader

.preheader:                                       ; preds = %187
  %188 = load i32, i32* %171, align 4
  %189 = sext i32 %188 to i64
  %190 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 %indvars.iv271, i64 %indvars.iv277, i64 %indvars.iv256, i64 %189
  %191 = load i32, i32* %190, align 4
  %192 = sext i32 %191 to i64
  %193 = getelementptr inbounds double, double* %tmor, i64 %192
  %194 = load double, double* %193, align 8
  %195 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv277, i64 %indvars.iv256, i64 %189
  %196 = load double, double* %195, align 8
  %197 = fmul double %196, 5.000000e-01
  %198 = fadd double %194, %197
  store double %198, double* %193, align 8
  %199 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv277, i64 %indvars.iv256, i64 1
  %200 = load double, double* %199, align 8
  %201 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv277, i64 %indvars.iv256, i64 2
  %202 = load double, double* %201, align 8
  %203 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv277, i64 %indvars.iv256, i64 3
  %204 = load double, double* %203, align 8
  %205 = load double, double* %172, align 8
  %206 = fmul double %205, %200
  %207 = fadd double %206, 0.000000e+00
  %208 = load double, double* %173, align 8
  %209 = fmul double %208, %202
  %210 = fadd double %207, %209
  %211 = load double, double* %174, align 8
  %212 = fmul double %211, %204
  %213 = fadd double %210, %212
  %214 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 %indvars.iv271, i64 %indvars.iv277, i64 %indvars.iv256, i64 0
  %215 = load i32, i32* %214, align 4
  %216 = sext i32 %215 to i64
  %217 = getelementptr inbounds double, double* %tmor, i64 %216
  %218 = load double, double* %217, align 8
  %219 = fadd double %213, %218
  store double %219, double* %217, align 8
  %220 = load double, double* %175, align 8
  %221 = fmul double %220, %200
  %222 = fadd double %221, 0.000000e+00
  %223 = load double, double* %176, align 8
  %224 = fmul double %223, %202
  %225 = fadd double %222, %224
  %226 = load double, double* %177, align 8
  %227 = fmul double %226, %204
  %228 = fadd double %225, %227
  %229 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 %indvars.iv271, i64 %indvars.iv277, i64 %indvars.iv256, i64 1
  %230 = load i32, i32* %229, align 4
  %231 = sext i32 %230 to i64
  %232 = getelementptr inbounds double, double* %tmor, i64 %231
  %233 = load double, double* %232, align 8
  %234 = fadd double %228, %233
  store double %234, double* %232, align 8
  %235 = load double, double* %178, align 8
  %236 = fmul double %235, %200
  %237 = fadd double %236, 0.000000e+00
  %238 = load double, double* %179, align 8
  %239 = fmul double %238, %202
  %240 = fadd double %237, %239
  %241 = load double, double* %180, align 8
  %242 = fmul double %241, %204
  %243 = fadd double %240, %242
  %244 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 %indvars.iv271, i64 %indvars.iv277, i64 %indvars.iv256, i64 2
  %245 = load i32, i32* %244, align 4
  %246 = sext i32 %245 to i64
  %247 = getelementptr inbounds double, double* %tmor, i64 %246
  %248 = load double, double* %247, align 8
  %249 = fadd double %243, %248
  store double %249, double* %247, align 8
  %250 = load double, double* %181, align 8
  %251 = fmul double %250, %200
  %252 = fadd double %251, 0.000000e+00
  %253 = load double, double* %182, align 8
  %254 = fmul double %253, %202
  %255 = fadd double %252, %254
  %256 = load double, double* %183, align 8
  %257 = fmul double %256, %204
  %258 = fadd double %255, %257
  %259 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 %indvars.iv271, i64 %indvars.iv277, i64 %indvars.iv256, i64 3
  %260 = load i32, i32* %259, align 4
  %261 = sext i32 %260 to i64
  %262 = getelementptr inbounds double, double* %tmor, i64 %261
  %263 = load double, double* %262, align 8
  %264 = fadd double %258, %263
  store double %264, double* %262, align 8
  %265 = load double, double* %184, align 8
  %266 = fmul double %265, %200
  %267 = fadd double %266, 0.000000e+00
  %268 = load double, double* %185, align 8
  %269 = fmul double %268, %202
  %270 = fadd double %267, %269
  %271 = load double, double* %186, align 8
  %272 = fmul double %271, %204
  %273 = fadd double %270, %272
  %274 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 %indvars.iv271, i64 %indvars.iv277, i64 %indvars.iv256, i64 4
  %275 = load i32, i32* %274, align 4
  %276 = sext i32 %275 to i64
  %277 = getelementptr inbounds double, double* %tmor, i64 %276
  %278 = load double, double* %277, align 8
  %279 = fadd double %273, %278
  store double %279, double* %277, align 8
  %indvars.iv.next257 = add nsw i64 %indvars.iv256, 1
  br label %187

280:                                              ; preds = %187
  %281 = load i32, i32* %162, align 4
  %282 = load i32, i32* %171, align 4
  %283 = sext i32 %282 to i64
  %284 = sext i32 %281 to i64
  %285 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 %indvars.iv271, i64 %indvars.iv277, i64 %284, i64 %283
  %286 = load i32, i32* %285, align 4
  %287 = sext i32 %286 to i64
  %288 = getelementptr inbounds double, double* %tmor, i64 %287
  %289 = load double, double* %288, align 8
  %290 = getelementptr inbounds [2 x [5 x double]], [2 x [5 x double]]* %top, i64 0, i64 %indvars.iv277, i64 %283
  %291 = load double, double* %290, align 8
  %292 = fmul double %291, 5.000000e-01
  %293 = fadd double %289, %292
  store double %293, double* %288, align 8
  %294 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv277, i64 %284, i64 1
  %295 = load double, double* %294, align 8
  %296 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv277, i64 %284, i64 2
  %297 = load double, double* %296, align 8
  %298 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv277, i64 %284, i64 3
  %299 = load double, double* %298, align 8
  %300 = load double, double* %172, align 8
  %301 = load double, double* %173, align 8
  %302 = load double, double* %174, align 8
  %303 = fmul double %300, %295
  %304 = fadd double %303, 0.000000e+00
  %305 = fmul double %301, %297
  %306 = fadd double %304, %305
  %307 = fmul double %302, %299
  %308 = fadd double %306, %307
  %309 = fmul double %300, %164
  %310 = fadd double %309, 0.000000e+00
  %311 = fmul double %301, %166
  %312 = fadd double %310, %311
  %313 = fmul double %302, %168
  %314 = fadd double %312, %313
  %315 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 %indvars.iv271, i64 %indvars.iv277, i64 %284, i64 0
  %316 = load i32, i32* %315, align 4
  %317 = sext i32 %316 to i64
  %318 = getelementptr inbounds double, double* %tmor, i64 %317
  %319 = load double, double* %318, align 8
  %320 = fmul double %308, 5.000000e-01
  %321 = fadd double %320, %319
  %322 = fadd double %314, %321
  store double %322, double* %318, align 8
  %323 = load double, double* %175, align 8
  %324 = load double, double* %176, align 8
  %325 = load double, double* %177, align 8
  %326 = fmul double %323, %295
  %327 = fadd double %326, 0.000000e+00
  %328 = fmul double %324, %297
  %329 = fadd double %327, %328
  %330 = fmul double %325, %299
  %331 = fadd double %329, %330
  %332 = fmul double %323, %164
  %333 = fadd double %332, 0.000000e+00
  %334 = fmul double %324, %166
  %335 = fadd double %333, %334
  %336 = fmul double %325, %168
  %337 = fadd double %335, %336
  %338 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 %indvars.iv271, i64 %indvars.iv277, i64 %284, i64 1
  %339 = load i32, i32* %338, align 4
  %340 = sext i32 %339 to i64
  %341 = getelementptr inbounds double, double* %tmor, i64 %340
  %342 = load double, double* %341, align 8
  %343 = fmul double %331, 5.000000e-01
  %344 = fadd double %343, %342
  %345 = fadd double %337, %344
  store double %345, double* %341, align 8
  %346 = load double, double* %178, align 8
  %347 = load double, double* %179, align 8
  %348 = load double, double* %180, align 8
  %349 = fmul double %346, %295
  %350 = fadd double %349, 0.000000e+00
  %351 = fmul double %347, %297
  %352 = fadd double %350, %351
  %353 = fmul double %348, %299
  %354 = fadd double %352, %353
  %355 = fmul double %346, %164
  %356 = fadd double %355, 0.000000e+00
  %357 = fmul double %347, %166
  %358 = fadd double %356, %357
  %359 = fmul double %348, %168
  %360 = fadd double %358, %359
  %361 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 %indvars.iv271, i64 %indvars.iv277, i64 %284, i64 2
  %362 = load i32, i32* %361, align 4
  %363 = sext i32 %362 to i64
  %364 = getelementptr inbounds double, double* %tmor, i64 %363
  %365 = load double, double* %364, align 8
  %366 = fmul double %354, 5.000000e-01
  %367 = fadd double %366, %365
  %368 = fadd double %360, %367
  store double %368, double* %364, align 8
  %369 = load double, double* %181, align 8
  %370 = load double, double* %182, align 8
  %371 = load double, double* %183, align 8
  %372 = fmul double %369, %295
  %373 = fadd double %372, 0.000000e+00
  %374 = fmul double %370, %297
  %375 = fadd double %373, %374
  %376 = fmul double %371, %299
  %377 = fadd double %375, %376
  %378 = fmul double %369, %164
  %379 = fadd double %378, 0.000000e+00
  %380 = fmul double %370, %166
  %381 = fadd double %379, %380
  %382 = fmul double %371, %168
  %383 = fadd double %381, %382
  %384 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 %indvars.iv271, i64 %indvars.iv277, i64 %284, i64 3
  %385 = load i32, i32* %384, align 4
  %386 = sext i32 %385 to i64
  %387 = getelementptr inbounds double, double* %tmor, i64 %386
  %388 = load double, double* %387, align 8
  %389 = fmul double %377, 5.000000e-01
  %390 = fadd double %389, %388
  %391 = fadd double %383, %390
  store double %391, double* %387, align 8
  %392 = load double, double* %184, align 8
  %393 = load double, double* %185, align 8
  %394 = load double, double* %186, align 8
  %395 = fmul double %392, %295
  %396 = fadd double %395, 0.000000e+00
  %397 = fmul double %393, %297
  %398 = fadd double %396, %397
  %399 = fmul double %394, %299
  %400 = fadd double %398, %399
  %401 = fmul double %392, %164
  %402 = fadd double %401, 0.000000e+00
  %403 = fmul double %393, %166
  %404 = fadd double %402, %403
  %405 = fmul double %394, %168
  %406 = fadd double %404, %405
  %407 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 %indvars.iv271, i64 %indvars.iv277, i64 %284, i64 4
  %408 = load i32, i32* %407, align 4
  %409 = sext i32 %408 to i64
  %410 = getelementptr inbounds double, double* %tmor, i64 %409
  %411 = load double, double* %410, align 8
  %412 = fmul double %400, 5.000000e-01
  %413 = fadd double %412, %411
  %414 = fadd double %406, %413
  store double %414, double* %410, align 8
  %indvars.iv.next272 = add nuw nsw i64 %indvars.iv271, 1
  br label %169

415:                                              ; preds = %169
  %indvars.iv.next278 = add nuw nsw i64 %indvars.iv277, 1
  %indvars.iv.next255 = add nsw i64 %indvars.iv254, -1
  %indvars.iv.next276 = add nsw i64 %indvars.iv275, -1
  br label %.preheader14

.preheader31.1:                                   ; preds = %7
  %416 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 1, i64 1
  %417 = load i32, i32* %416, align 4
  %418 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 1, i64 1
  %419 = load i32, i32* %418, align 4
  %420 = sext i32 %419 to i64
  %421 = getelementptr inbounds double, double* %tmor, i64 %420
  %422 = load double, double* %421, align 8
  %423 = sext i32 %417 to i64
  %424 = getelementptr inbounds double, double* %tx, i64 %423
  %425 = load double, double* %424, align 8
  %426 = fadd double %422, %425
  store double %426, double* %421, align 8
  %427 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 1, i64 2
  %428 = load i32, i32* %427, align 4
  %429 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 1, i64 2
  %430 = load i32, i32* %429, align 4
  %431 = sext i32 %430 to i64
  %432 = getelementptr inbounds double, double* %tmor, i64 %431
  %433 = load double, double* %432, align 8
  %434 = sext i32 %428 to i64
  %435 = getelementptr inbounds double, double* %tx, i64 %434
  %436 = load double, double* %435, align 8
  %437 = fadd double %433, %436
  store double %437, double* %432, align 8
  %438 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 1, i64 3
  %439 = load i32, i32* %438, align 4
  %440 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 1, i64 3
  %441 = load i32, i32* %440, align 4
  %442 = sext i32 %441 to i64
  %443 = getelementptr inbounds double, double* %tmor, i64 %442
  %444 = load double, double* %443, align 8
  %445 = sext i32 %439 to i64
  %446 = getelementptr inbounds double, double* %tx, i64 %445
  %447 = load double, double* %446, align 8
  %448 = fadd double %444, %447
  store double %448, double* %443, align 8
  %449 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 2, i64 1
  %450 = load i32, i32* %449, align 4
  %451 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 2, i64 1
  %452 = load i32, i32* %451, align 4
  %453 = sext i32 %452 to i64
  %454 = getelementptr inbounds double, double* %tmor, i64 %453
  %455 = load double, double* %454, align 8
  %456 = sext i32 %450 to i64
  %457 = getelementptr inbounds double, double* %tx, i64 %456
  %458 = load double, double* %457, align 8
  %459 = fadd double %455, %458
  store double %459, double* %454, align 8
  %460 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 2, i64 2
  %461 = load i32, i32* %460, align 4
  %462 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 2, i64 2
  %463 = load i32, i32* %462, align 8
  %464 = sext i32 %463 to i64
  %465 = getelementptr inbounds double, double* %tmor, i64 %464
  %466 = load double, double* %465, align 8
  %467 = sext i32 %461 to i64
  %468 = getelementptr inbounds double, double* %tx, i64 %467
  %469 = load double, double* %468, align 8
  %470 = fadd double %466, %469
  store double %470, double* %465, align 8
  %471 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 2, i64 3
  %472 = load i32, i32* %471, align 4
  %473 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 2, i64 3
  %474 = load i32, i32* %473, align 4
  %475 = sext i32 %474 to i64
  %476 = getelementptr inbounds double, double* %tmor, i64 %475
  %477 = load double, double* %476, align 8
  %478 = sext i32 %472 to i64
  %479 = getelementptr inbounds double, double* %tx, i64 %478
  %480 = load double, double* %479, align 8
  %481 = fadd double %477, %480
  store double %481, double* %476, align 8
  %482 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 3, i64 1
  %483 = load i32, i32* %482, align 4
  %484 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 3, i64 1
  %485 = load i32, i32* %484, align 4
  %486 = sext i32 %485 to i64
  %487 = getelementptr inbounds double, double* %tmor, i64 %486
  %488 = load double, double* %487, align 8
  %489 = sext i32 %483 to i64
  %490 = getelementptr inbounds double, double* %tx, i64 %489
  %491 = load double, double* %490, align 8
  %492 = fadd double %488, %491
  store double %492, double* %487, align 8
  %493 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 3, i64 2
  %494 = load i32, i32* %493, align 4
  %495 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 3, i64 2
  %496 = load i32, i32* %495, align 4
  %497 = sext i32 %496 to i64
  %498 = getelementptr inbounds double, double* %tmor, i64 %497
  %499 = load double, double* %498, align 8
  %500 = sext i32 %494 to i64
  %501 = getelementptr inbounds double, double* %tx, i64 %500
  %502 = load double, double* %501, align 8
  %503 = fadd double %499, %502
  store double %503, double* %498, align 8
  %504 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 3, i64 3
  %505 = load i32, i32* %504, align 4
  %506 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 3, i64 3
  %507 = load i32, i32* %506, align 4
  %508 = sext i32 %507 to i64
  %509 = getelementptr inbounds double, double* %tmor, i64 %508
  %510 = load double, double* %509, align 8
  %511 = sext i32 %505 to i64
  %512 = getelementptr inbounds double, double* %tx, i64 %511
  %513 = load double, double* %512, align 8
  %514 = fadd double %510, %513
  store double %514, double* %509, align 8
  %515 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 0, i64 4
  %516 = load i32, i32* %515, align 16
  %517 = icmp eq i32 %516, -1
  %518 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 1
  br i1 %517, label %.loopexit28.loopexit, label %.preheader29.preheader

.preheader29.preheader:                           ; preds = %.preheader31.1
  %519 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 2
  %520 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 3
  br label %.preheader12

.preheader12:                                     ; preds = %.preheader6, %.preheader29.preheader
  %indvars.iv50 = phi i64 [ %indvars.iv.next51, %.preheader6 ], [ 0, %.preheader29.preheader ]
  %exitcond52 = icmp eq i64 %indvars.iv50, 5
  br i1 %exitcond52, label %.preheader12.1, label %.preheader6

.preheader6:                                      ; preds = %.preheader12
  %521 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv50, i64 0
  %522 = load double, double* %521, align 8
  %523 = load i32, i32* %518, align 4
  %524 = sext i32 %523 to i64
  %525 = getelementptr inbounds double, double* %tx, i64 %524
  %526 = load double, double* %525, align 8
  %527 = fmul double %522, %526
  %528 = fadd double %527, 0.000000e+00
  %529 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv50, i64 1
  %530 = load double, double* %529, align 8
  %531 = load i32, i32* %519, align 4
  %532 = sext i32 %531 to i64
  %533 = getelementptr inbounds double, double* %tx, i64 %532
  %534 = load double, double* %533, align 8
  %535 = fmul double %530, %534
  %536 = fadd double %528, %535
  %537 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv50, i64 2
  %538 = load double, double* %537, align 8
  %539 = load i32, i32* %520, align 4
  %540 = sext i32 %539 to i64
  %541 = getelementptr inbounds double, double* %tx, i64 %540
  %542 = load double, double* %541, align 8
  %543 = fmul double %538, %542
  %544 = fadd double %536, %543
  %545 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 0, i64 %indvars.iv50
  %546 = load i32, i32* %545, align 4
  %547 = sext i32 %546 to i64
  %548 = getelementptr inbounds double, double* %tmor, i64 %547
  %549 = load double, double* %548, align 8
  %550 = fmul double %544, 5.000000e-01
  %551 = fadd double %550, %549
  store double %551, double* %548, align 8
  %indvars.iv.next51 = add nuw nsw i64 %indvars.iv50, 1
  br label %.preheader12

.loopexit28.loopexit:                             ; preds = %.preheader31.1
  %552 = load i32, i32* %518, align 4
  %553 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 0, i64 1
  %554 = load i32, i32* %553, align 4
  %555 = sext i32 %554 to i64
  %556 = getelementptr inbounds double, double* %tmor, i64 %555
  %557 = load double, double* %556, align 8
  %558 = sext i32 %552 to i64
  %559 = getelementptr inbounds double, double* %tx, i64 %558
  %560 = load double, double* %559, align 8
  %561 = fmul double %560, 5.000000e-01
  %562 = fadd double %557, %561
  store double %562, double* %556, align 8
  %563 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 2
  %564 = load i32, i32* %563, align 4
  %565 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 0, i64 2
  %566 = load i32, i32* %565, align 8
  %567 = sext i32 %566 to i64
  %568 = getelementptr inbounds double, double* %tmor, i64 %567
  %569 = load double, double* %568, align 8
  %570 = sext i32 %564 to i64
  %571 = getelementptr inbounds double, double* %tx, i64 %570
  %572 = load double, double* %571, align 8
  %573 = fmul double %572, 5.000000e-01
  %574 = fadd double %569, %573
  store double %574, double* %568, align 8
  %575 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 3
  %576 = load i32, i32* %575, align 4
  %577 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 0, i64 3
  %578 = load i32, i32* %577, align 4
  %579 = sext i32 %578 to i64
  %580 = getelementptr inbounds double, double* %tmor, i64 %579
  %581 = load double, double* %580, align 8
  %582 = sext i32 %576 to i64
  %583 = getelementptr inbounds double, double* %tx, i64 %582
  %584 = load double, double* %583, align 8
  %585 = fmul double %584, 5.000000e-01
  %586 = fadd double %581, %585
  store double %586, double* %580, align 8
  br label %.loopexit28

.loopexit28:                                      ; preds = %.preheader12.1, %.loopexit28.loopexit
  %587 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 1, i64 0, i64 1, i64 4
  %588 = load i32, i32* %587, align 4
  %589 = icmp eq i32 %588, -1
  %590 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 1, i64 4
  br i1 %589, label %.loopexit24.loopexit, label %.preheader25.preheader

.preheader25.preheader:                           ; preds = %.loopexit28
  %591 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 2, i64 4
  %592 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 3, i64 4
  br label %.preheader11

.preheader11:                                     ; preds = %.preheader5, %.preheader25.preheader
  %indvars.iv75 = phi i64 [ %indvars.iv.next76, %.preheader5 ], [ 0, %.preheader25.preheader ]
  %exitcond77 = icmp eq i64 %indvars.iv75, 5
  br i1 %exitcond77, label %.preheader11.1, label %.preheader5

.preheader5:                                      ; preds = %.preheader11
  %593 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv75, i64 0
  %594 = load double, double* %593, align 8
  %595 = load i32, i32* %590, align 4
  %596 = sext i32 %595 to i64
  %597 = getelementptr inbounds double, double* %tx, i64 %596
  %598 = load double, double* %597, align 8
  %599 = fmul double %594, %598
  %600 = fadd double %599, 0.000000e+00
  %601 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv75, i64 1
  %602 = load double, double* %601, align 8
  %603 = load i32, i32* %591, align 4
  %604 = sext i32 %603 to i64
  %605 = getelementptr inbounds double, double* %tx, i64 %604
  %606 = load double, double* %605, align 8
  %607 = fmul double %602, %606
  %608 = fadd double %600, %607
  %609 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv75, i64 2
  %610 = load double, double* %609, align 8
  %611 = load i32, i32* %592, align 4
  %612 = sext i32 %611 to i64
  %613 = getelementptr inbounds double, double* %tx, i64 %612
  %614 = load double, double* %613, align 8
  %615 = fmul double %610, %614
  %616 = fadd double %608, %615
  %617 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 1, i64 0, i64 %indvars.iv75, i64 4
  %618 = load i32, i32* %617, align 4
  %619 = sext i32 %618 to i64
  %620 = getelementptr inbounds double, double* %tmor, i64 %619
  %621 = load double, double* %620, align 8
  %622 = fmul double %616, 5.000000e-01
  %623 = fadd double %622, %621
  store double %623, double* %620, align 8
  %indvars.iv.next76 = add nuw nsw i64 %indvars.iv75, 1
  br label %.preheader11

.loopexit24.loopexit:                             ; preds = %.loopexit28
  %624 = load i32, i32* %590, align 4
  %625 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 1, i64 4
  %626 = load i32, i32* %625, align 4
  %627 = sext i32 %626 to i64
  %628 = getelementptr inbounds double, double* %tmor, i64 %627
  %629 = load double, double* %628, align 8
  %630 = sext i32 %624 to i64
  %631 = getelementptr inbounds double, double* %tx, i64 %630
  %632 = load double, double* %631, align 8
  %633 = fmul double %632, 5.000000e-01
  %634 = fadd double %629, %633
  store double %634, double* %628, align 8
  %635 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 2, i64 4
  %636 = load i32, i32* %635, align 4
  %637 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 2, i64 4
  %638 = load i32, i32* %637, align 8
  %639 = sext i32 %638 to i64
  %640 = getelementptr inbounds double, double* %tmor, i64 %639
  %641 = load double, double* %640, align 8
  %642 = sext i32 %636 to i64
  %643 = getelementptr inbounds double, double* %tx, i64 %642
  %644 = load double, double* %643, align 8
  %645 = fmul double %644, 5.000000e-01
  %646 = fadd double %641, %645
  store double %646, double* %640, align 8
  %647 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 3, i64 4
  %648 = load i32, i32* %647, align 4
  %649 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 3, i64 4
  %650 = load i32, i32* %649, align 4
  %651 = sext i32 %650 to i64
  %652 = getelementptr inbounds double, double* %tmor, i64 %651
  %653 = load double, double* %652, align 8
  %654 = sext i32 %648 to i64
  %655 = getelementptr inbounds double, double* %tx, i64 %654
  %656 = load double, double* %655, align 8
  %657 = fmul double %656, 5.000000e-01
  %658 = fadd double %653, %657
  store double %658, double* %652, align 8
  br label %.loopexit24

.loopexit24:                                      ; preds = %.preheader11.1, %.loopexit24.loopexit
  %659 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 1, i64 4, i64 1
  %660 = load i32, i32* %659, align 4
  %661 = icmp eq i32 %660, -1
  %662 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 4, i64 1
  br i1 %661, label %.loopexit20.loopexit, label %.preheader21.preheader

.preheader21.preheader:                           ; preds = %.loopexit24
  %663 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 4, i64 2
  %664 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 4, i64 3
  br label %.preheader10

.preheader10:                                     ; preds = %.preheader4, %.preheader21.preheader
  %indvars.iv108 = phi i64 [ %indvars.iv.next109, %.preheader4 ], [ 0, %.preheader21.preheader ]
  %exitcond110 = icmp eq i64 %indvars.iv108, 5
  br i1 %exitcond110, label %.preheader10.1, label %.preheader4

.preheader4:                                      ; preds = %.preheader10
  %665 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv108, i64 0
  %666 = load double, double* %665, align 8
  %667 = load i32, i32* %662, align 4
  %668 = sext i32 %667 to i64
  %669 = getelementptr inbounds double, double* %tx, i64 %668
  %670 = load double, double* %669, align 8
  %671 = fmul double %666, %670
  %672 = fadd double %671, 0.000000e+00
  %673 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv108, i64 1
  %674 = load double, double* %673, align 8
  %675 = load i32, i32* %663, align 4
  %676 = sext i32 %675 to i64
  %677 = getelementptr inbounds double, double* %tx, i64 %676
  %678 = load double, double* %677, align 8
  %679 = fmul double %674, %678
  %680 = fadd double %672, %679
  %681 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv108, i64 2
  %682 = load double, double* %681, align 8
  %683 = load i32, i32* %664, align 4
  %684 = sext i32 %683 to i64
  %685 = getelementptr inbounds double, double* %tx, i64 %684
  %686 = load double, double* %685, align 8
  %687 = fmul double %682, %686
  %688 = fadd double %680, %687
  %689 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 1, i64 4, i64 %indvars.iv108
  %690 = load i32, i32* %689, align 4
  %691 = sext i32 %690 to i64
  %692 = getelementptr inbounds double, double* %tmor, i64 %691
  %693 = load double, double* %692, align 8
  %694 = fmul double %688, 5.000000e-01
  %695 = fadd double %694, %693
  store double %695, double* %692, align 8
  %indvars.iv.next109 = add nuw nsw i64 %indvars.iv108, 1
  br label %.preheader10

.loopexit20.loopexit:                             ; preds = %.loopexit24
  %696 = load i32, i32* %662, align 4
  %697 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 4, i64 1
  %698 = load i32, i32* %697, align 4
  %699 = sext i32 %698 to i64
  %700 = getelementptr inbounds double, double* %tmor, i64 %699
  %701 = load double, double* %700, align 8
  %702 = sext i32 %696 to i64
  %703 = getelementptr inbounds double, double* %tx, i64 %702
  %704 = load double, double* %703, align 8
  %705 = fmul double %704, 5.000000e-01
  %706 = fadd double %701, %705
  store double %706, double* %700, align 8
  %707 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 4, i64 2
  %708 = load i32, i32* %707, align 4
  %709 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 4, i64 2
  %710 = load i32, i32* %709, align 8
  %711 = sext i32 %710 to i64
  %712 = getelementptr inbounds double, double* %tmor, i64 %711
  %713 = load double, double* %712, align 8
  %714 = sext i32 %708 to i64
  %715 = getelementptr inbounds double, double* %tx, i64 %714
  %716 = load double, double* %715, align 8
  %717 = fmul double %716, 5.000000e-01
  %718 = fadd double %713, %717
  store double %718, double* %712, align 8
  %719 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 4, i64 3
  %720 = load i32, i32* %719, align 4
  %721 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 4, i64 3
  %722 = load i32, i32* %721, align 4
  %723 = sext i32 %722 to i64
  %724 = getelementptr inbounds double, double* %tmor, i64 %723
  %725 = load double, double* %724, align 8
  %726 = sext i32 %720 to i64
  %727 = getelementptr inbounds double, double* %tx, i64 %726
  %728 = load double, double* %727, align 8
  %729 = fmul double %728, 5.000000e-01
  %730 = fadd double %725, %729
  store double %730, double* %724, align 8
  br label %.loopexit20

.loopexit20:                                      ; preds = %.preheader10.1, %.loopexit20.loopexit
  %731 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 4, i64 0
  %732 = load i32, i32* %731, align 16
  %733 = icmp eq i32 %732, -1
  %734 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 1, i64 0
  br i1 %733, label %.loopexit.loopexit35, label %.preheader17.preheader

.preheader17.preheader:                           ; preds = %.loopexit20
  %735 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 2, i64 0
  %736 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 3, i64 0
  br label %.preheader9

.preheader9:                                      ; preds = %.preheader3, %.preheader17.preheader
  %indvars.iv149 = phi i64 [ %indvars.iv.next150, %.preheader3 ], [ 0, %.preheader17.preheader ]
  %exitcond151 = icmp eq i64 %indvars.iv149, 5
  br i1 %exitcond151, label %.preheader9.1, label %.preheader3

.preheader3:                                      ; preds = %.preheader9
  %737 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv149, i64 0
  %738 = load double, double* %737, align 8
  %739 = load i32, i32* %734, align 4
  %740 = sext i32 %739 to i64
  %741 = getelementptr inbounds double, double* %tx, i64 %740
  %742 = load double, double* %741, align 8
  %743 = fmul double %738, %742
  %744 = fadd double %743, 0.000000e+00
  %745 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv149, i64 1
  %746 = load double, double* %745, align 8
  %747 = load i32, i32* %735, align 4
  %748 = sext i32 %747 to i64
  %749 = getelementptr inbounds double, double* %tx, i64 %748
  %750 = load double, double* %749, align 8
  %751 = fmul double %746, %750
  %752 = fadd double %744, %751
  %753 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv149, i64 2
  %754 = load double, double* %753, align 8
  %755 = load i32, i32* %736, align 4
  %756 = sext i32 %755 to i64
  %757 = getelementptr inbounds double, double* %tx, i64 %756
  %758 = load double, double* %757, align 8
  %759 = fmul double %754, %758
  %760 = fadd double %752, %759
  %761 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 %indvars.iv149, i64 0
  %762 = load i32, i32* %761, align 4
  %763 = sext i32 %762 to i64
  %764 = getelementptr inbounds double, double* %tmor, i64 %763
  %765 = load double, double* %764, align 8
  %766 = fmul double %760, 5.000000e-01
  %767 = fadd double %766, %765
  store double %767, double* %764, align 8
  %indvars.iv.next150 = add nuw nsw i64 %indvars.iv149, 1
  br label %.preheader9

.loopexit.loopexit35:                             ; preds = %.loopexit20
  %768 = load i32, i32* %734, align 4
  %769 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 1, i64 0
  %770 = load i32, i32* %769, align 4
  %771 = sext i32 %770 to i64
  %772 = getelementptr inbounds double, double* %tmor, i64 %771
  %773 = load double, double* %772, align 8
  %774 = sext i32 %768 to i64
  %775 = getelementptr inbounds double, double* %tx, i64 %774
  %776 = load double, double* %775, align 8
  %777 = fmul double %776, 5.000000e-01
  %778 = fadd double %773, %777
  store double %778, double* %772, align 8
  %779 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 2, i64 0
  %780 = load i32, i32* %779, align 4
  %781 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 2, i64 0
  %782 = load i32, i32* %781, align 8
  %783 = sext i32 %782 to i64
  %784 = getelementptr inbounds double, double* %tmor, i64 %783
  %785 = load double, double* %784, align 8
  %786 = sext i32 %780 to i64
  %787 = getelementptr inbounds double, double* %tx, i64 %786
  %788 = load double, double* %787, align 8
  %789 = fmul double %788, 5.000000e-01
  %790 = fadd double %785, %789
  store double %790, double* %784, align 8
  %791 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 3, i64 0
  %792 = load i32, i32* %791, align 4
  %793 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 0, i64 3, i64 0
  %794 = load i32, i32* %793, align 4
  %795 = sext i32 %794 to i64
  %796 = getelementptr inbounds double, double* %tmor, i64 %795
  %797 = load double, double* %796, align 8
  %798 = sext i32 %792 to i64
  %799 = getelementptr inbounds double, double* %tx, i64 %798
  %800 = load double, double* %799, align 8
  %801 = fmul double %800, 5.000000e-01
  %802 = fadd double %797, %801
  store double %802, double* %796, align 8
  br label %.loopexit

.loopexit:                                        ; preds = %.preheader9.1, %.loopexit.loopexit35, %.preheader14
  %indvars.iv.next282 = add nuw nsw i64 %indvars.iv281, 1
  br label %.preheader32

803:                                              ; preds = %.preheader32
  %indvars.iv.next285 = add nuw nsw i64 %indvars.iv284, 1
  br label %3

804:                                              ; preds = %3
  ret void

.preheader12.1:                                   ; preds = %.preheader6.1, %.preheader12
  %indvars.iv50.1 = phi i64 [ %indvars.iv.next51.1, %.preheader6.1 ], [ 0, %.preheader12 ]
  %exitcond52.1 = icmp eq i64 %indvars.iv50.1, 5
  br i1 %exitcond52.1, label %.loopexit28, label %.preheader6.1

.preheader6.1:                                    ; preds = %.preheader12.1
  %805 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 %indvars.iv50.1, i64 0
  %806 = load double, double* %805, align 8
  %807 = load i32, i32* %518, align 4
  %808 = sext i32 %807 to i64
  %809 = getelementptr inbounds double, double* %tx, i64 %808
  %810 = load double, double* %809, align 8
  %811 = fmul double %806, %810
  %812 = fadd double %811, 0.000000e+00
  %813 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 %indvars.iv50.1, i64 1
  %814 = load double, double* %813, align 8
  %815 = load i32, i32* %519, align 4
  %816 = sext i32 %815 to i64
  %817 = getelementptr inbounds double, double* %tx, i64 %816
  %818 = load double, double* %817, align 8
  %819 = fmul double %814, %818
  %820 = fadd double %812, %819
  %821 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 %indvars.iv50.1, i64 2
  %822 = load double, double* %821, align 8
  %823 = load i32, i32* %520, align 4
  %824 = sext i32 %823 to i64
  %825 = getelementptr inbounds double, double* %tx, i64 %824
  %826 = load double, double* %825, align 8
  %827 = fmul double %822, %826
  %828 = fadd double %820, %827
  %829 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 1, i64 0, i64 0, i64 %indvars.iv50.1
  %830 = load i32, i32* %829, align 4
  %831 = sext i32 %830 to i64
  %832 = getelementptr inbounds double, double* %tmor, i64 %831
  %833 = load double, double* %832, align 8
  %834 = fmul double %828, 5.000000e-01
  %835 = fadd double %834, %833
  store double %835, double* %832, align 8
  %indvars.iv.next51.1 = add nuw nsw i64 %indvars.iv50.1, 1
  br label %.preheader12.1

.preheader11.1:                                   ; preds = %.preheader5.1, %.preheader11
  %indvars.iv75.1 = phi i64 [ %indvars.iv.next76.1, %.preheader5.1 ], [ 0, %.preheader11 ]
  %exitcond77.1 = icmp eq i64 %indvars.iv75.1, 5
  br i1 %exitcond77.1, label %.loopexit24, label %.preheader5.1

.preheader5.1:                                    ; preds = %.preheader11.1
  %836 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 %indvars.iv75.1, i64 0
  %837 = load double, double* %836, align 8
  %838 = load i32, i32* %590, align 4
  %839 = sext i32 %838 to i64
  %840 = getelementptr inbounds double, double* %tx, i64 %839
  %841 = load double, double* %840, align 8
  %842 = fmul double %837, %841
  %843 = fadd double %842, 0.000000e+00
  %844 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 %indvars.iv75.1, i64 1
  %845 = load double, double* %844, align 8
  %846 = load i32, i32* %591, align 4
  %847 = sext i32 %846 to i64
  %848 = getelementptr inbounds double, double* %tx, i64 %847
  %849 = load double, double* %848, align 8
  %850 = fmul double %845, %849
  %851 = fadd double %843, %850
  %852 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 %indvars.iv75.1, i64 2
  %853 = load double, double* %852, align 8
  %854 = load i32, i32* %592, align 4
  %855 = sext i32 %854 to i64
  %856 = getelementptr inbounds double, double* %tx, i64 %855
  %857 = load double, double* %856, align 8
  %858 = fmul double %853, %857
  %859 = fadd double %851, %858
  %860 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 1, i64 1, i64 %indvars.iv75.1, i64 4
  %861 = load i32, i32* %860, align 4
  %862 = sext i32 %861 to i64
  %863 = getelementptr inbounds double, double* %tmor, i64 %862
  %864 = load double, double* %863, align 8
  %865 = fmul double %859, 5.000000e-01
  %866 = fadd double %865, %864
  store double %866, double* %863, align 8
  %indvars.iv.next76.1 = add nuw nsw i64 %indvars.iv75.1, 1
  br label %.preheader11.1

.preheader10.1:                                   ; preds = %.preheader4.1, %.preheader10
  %indvars.iv108.1 = phi i64 [ %indvars.iv.next109.1, %.preheader4.1 ], [ 0, %.preheader10 ]
  %exitcond110.1 = icmp eq i64 %indvars.iv108.1, 5
  br i1 %exitcond110.1, label %.loopexit20, label %.preheader4.1

.preheader4.1:                                    ; preds = %.preheader10.1
  %867 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 %indvars.iv108.1, i64 0
  %868 = load double, double* %867, align 8
  %869 = load i32, i32* %662, align 4
  %870 = sext i32 %869 to i64
  %871 = getelementptr inbounds double, double* %tx, i64 %870
  %872 = load double, double* %871, align 8
  %873 = fmul double %868, %872
  %874 = fadd double %873, 0.000000e+00
  %875 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 %indvars.iv108.1, i64 1
  %876 = load double, double* %875, align 8
  %877 = load i32, i32* %663, align 4
  %878 = sext i32 %877 to i64
  %879 = getelementptr inbounds double, double* %tx, i64 %878
  %880 = load double, double* %879, align 8
  %881 = fmul double %876, %880
  %882 = fadd double %874, %881
  %883 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 %indvars.iv108.1, i64 2
  %884 = load double, double* %883, align 8
  %885 = load i32, i32* %664, align 4
  %886 = sext i32 %885 to i64
  %887 = getelementptr inbounds double, double* %tx, i64 %886
  %888 = load double, double* %887, align 8
  %889 = fmul double %884, %888
  %890 = fadd double %882, %889
  %891 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 1, i64 1, i64 4, i64 %indvars.iv108.1
  %892 = load i32, i32* %891, align 4
  %893 = sext i32 %892 to i64
  %894 = getelementptr inbounds double, double* %tmor, i64 %893
  %895 = load double, double* %894, align 8
  %896 = fmul double %890, 5.000000e-01
  %897 = fadd double %896, %895
  store double %897, double* %894, align 8
  %indvars.iv.next109.1 = add nuw nsw i64 %indvars.iv108.1, 1
  br label %.preheader10.1

.preheader9.1:                                    ; preds = %.preheader3.1, %.preheader9
  %indvars.iv149.1 = phi i64 [ %indvars.iv.next150.1, %.preheader3.1 ], [ 0, %.preheader9 ]
  %exitcond151.1 = icmp eq i64 %indvars.iv149.1, 5
  br i1 %exitcond151.1, label %.loopexit, label %.preheader3.1

.preheader3.1:                                    ; preds = %.preheader9.1
  %898 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 %indvars.iv149.1, i64 0
  %899 = load double, double* %898, align 8
  %900 = load i32, i32* %734, align 4
  %901 = sext i32 %900 to i64
  %902 = getelementptr inbounds double, double* %tx, i64 %901
  %903 = load double, double* %902, align 8
  %904 = fmul double %899, %903
  %905 = fadd double %904, 0.000000e+00
  %906 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 %indvars.iv149.1, i64 1
  %907 = load double, double* %906, align 8
  %908 = load i32, i32* %735, align 4
  %909 = sext i32 %908 to i64
  %910 = getelementptr inbounds double, double* %tx, i64 %909
  %911 = load double, double* %910, align 8
  %912 = fmul double %907, %911
  %913 = fadd double %905, %912
  %914 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 1, i64 %indvars.iv149.1, i64 2
  %915 = load double, double* %914, align 8
  %916 = load i32, i32* %736, align 4
  %917 = sext i32 %916 to i64
  %918 = getelementptr inbounds double, double* %tx, i64 %917
  %919 = load double, double* %918, align 8
  %920 = fmul double %915, %919
  %921 = fadd double %913, %920
  %922 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv284, i64 %indvars.iv281, i64 0, i64 1, i64 %indvars.iv149.1, i64 0
  %923 = load i32, i32* %922, align 4
  %924 = sext i32 %923 to i64
  %925 = getelementptr inbounds double, double* %tmor, i64 %924
  %926 = load double, double* %925, align 8
  %927 = fmul double %921, 5.000000e-01
  %928 = fadd double %927, %926
  store double %928, double* %925, align 8
  %indvars.iv.next150.1 = add nuw nsw i64 %indvars.iv149.1, 1
  br label %.preheader9.1
}

; Function Attrs: nofree norecurse nounwind uwtable
define void @transfb_cor_e(i32 %n, double* nocapture %tmor, [5 x [5 x double]]* nocapture readonly %tx) local_unnamed_addr #2 {
  %1 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 0
  %2 = load double, double* %1, align 8
  %3 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %4 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 1
  %5 = load double, double* %4, align 8
  %6 = fmul double %3, %5
  %7 = fadd double %2, %6
  %8 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %9 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 2
  %10 = load double, double* %9, align 8
  %11 = fmul double %8, %10
  %12 = fadd double %7, %11
  %13 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %14 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 3
  %15 = load double, double* %14, align 8
  %16 = fmul double %13, %15
  %17 = fadd double %12, %16
  %18 = icmp sgt i32 %n, 1
  br i1 %18, label %19, label %.thread

19:                                               ; preds = %0
  %20 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 1, i64 0
  %21 = load double, double* %20, align 8
  %22 = fmul double %3, %21
  %23 = fadd double %17, %22
  %24 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 2, i64 0
  %25 = load double, double* %24, align 8
  %26 = fmul double %8, %25
  %27 = fadd double %23, %26
  %28 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 3, i64 0
  %29 = load double, double* %28, align 8
  %30 = fmul double %13, %29
  %31 = fadd double %27, %30
  %32 = icmp eq i32 %n, 3
  br i1 %32, label %.thread.loopexit, label %.thread

.thread.loopexit:                                 ; preds = %19
  %33 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 1, i64 0, i64 0
  %34 = load double, double* %33, align 8
  %35 = fmul double %3, %34
  %36 = fadd double %31, %35
  %37 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 2, i64 0, i64 0
  %38 = load double, double* %37, align 8
  %39 = fmul double %8, %38
  %40 = fadd double %36, %39
  %41 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 3, i64 0, i64 0
  %42 = load double, double* %41, align 8
  %43 = fmul double %13, %42
  %44 = fadd double %40, %43
  br label %.thread

.thread:                                          ; preds = %.thread.loopexit, %19, %0
  %tmp.4 = phi double [ %31, %19 ], [ %17, %0 ], [ %44, %.thread.loopexit ]
  store double %tmp.4, double* %tmor, align 8
  ret void
}

; Function Attrs: nounwind uwtable
define void @transfb_cor_f(i32 %n, double* nocapture %tmor, [5 x [5 x double]]* nocapture readonly %tx) local_unnamed_addr #0 {
  %temp = alloca [5 x double], align 16
  %1 = getelementptr inbounds [5 x double], [5 x double]* %temp, i64 0, i64 0
  call void @r_init(double* nonnull %1, i32 5, double 0.000000e+00) #4
  %2 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %3 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %4 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %5 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 0
  %6 = load double, double* %5, align 8
  %7 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 1, i64 0
  %8 = load double, double* %7, align 8
  %9 = fmul double %2, %8
  %10 = fadd double %9, %6
  %11 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 2, i64 0
  %12 = load double, double* %11, align 8
  %13 = fmul double %3, %12
  %14 = fadd double %10, %13
  %15 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 3, i64 0
  %16 = load double, double* %15, align 8
  %17 = fmul double %4, %16
  %18 = fadd double %14, %17
  store double %18, double* %1, align 16
  %19 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 1
  %20 = load double, double* %19, align 8
  %21 = getelementptr inbounds [5 x double], [5 x double]* %temp, i64 0, i64 1
  %22 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 1, i64 1
  %23 = load double, double* %22, align 8
  %24 = fmul double %2, %23
  %25 = fadd double %24, %20
  %26 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 2, i64 1
  %27 = load double, double* %26, align 8
  %28 = fmul double %3, %27
  %29 = fadd double %25, %28
  %30 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 3, i64 1
  %31 = load double, double* %30, align 8
  %32 = fmul double %4, %31
  %33 = fadd double %29, %32
  store double %33, double* %21, align 8
  %34 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 2
  %35 = load double, double* %34, align 8
  %36 = getelementptr inbounds [5 x double], [5 x double]* %temp, i64 0, i64 2
  %37 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 1, i64 2
  %38 = load double, double* %37, align 8
  %39 = fmul double %2, %38
  %40 = fadd double %39, %35
  %41 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 2, i64 2
  %42 = load double, double* %41, align 8
  %43 = fmul double %3, %42
  %44 = fadd double %40, %43
  %45 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 3, i64 2
  %46 = load double, double* %45, align 8
  %47 = fmul double %4, %46
  %48 = fadd double %44, %47
  store double %48, double* %36, align 16
  %49 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 3
  %50 = load double, double* %49, align 8
  %51 = getelementptr inbounds [5 x double], [5 x double]* %temp, i64 0, i64 3
  %52 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 1, i64 3
  %53 = load double, double* %52, align 8
  %54 = fmul double %2, %53
  %55 = fadd double %54, %50
  %56 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 2, i64 3
  %57 = load double, double* %56, align 8
  %58 = fmul double %3, %57
  %59 = fadd double %55, %58
  %60 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 3, i64 3
  %61 = load double, double* %60, align 8
  %62 = fmul double %4, %61
  %63 = fadd double %59, %62
  store double %63, double* %51, align 8
  %64 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 4
  %65 = load double, double* %64, align 8
  %66 = getelementptr inbounds [5 x double], [5 x double]* %temp, i64 0, i64 4
  %67 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 1, i64 4
  %68 = load double, double* %67, align 8
  %69 = fmul double %2, %68
  %70 = fadd double %69, %65
  %71 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 2, i64 4
  %72 = load double, double* %71, align 8
  %73 = fmul double %3, %72
  %74 = fadd double %70, %73
  %75 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 3, i64 4
  %76 = load double, double* %75, align 8
  %77 = fmul double %4, %76
  %78 = fadd double %74, %77
  store double %78, double* %66, align 16
  %79 = load double, double* %1, align 16
  %80 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %81 = load double, double* %21, align 8
  %82 = fmul double %80, %81
  %83 = fadd double %79, %82
  %84 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %85 = load double, double* %36, align 16
  %86 = fmul double %84, %85
  %87 = fadd double %83, %86
  %88 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %89 = load double, double* %51, align 8
  %90 = fmul double %88, %89
  %91 = fadd double %87, %90
  %92 = icmp eq i32 %n, 5
  br i1 %92, label %.loopexit.thread, label %.loopexit

.loopexit.thread:                                 ; preds = %0
  %93 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 1, i64 0, i64 0
  %94 = load double, double* %93, align 8
  %95 = fmul double %80, %94
  %96 = fadd double %91, %95
  %97 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 2, i64 0, i64 0
  %98 = load double, double* %97, align 8
  %99 = fmul double %84, %98
  %100 = fadd double %96, %99
  %101 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 3, i64 0, i64 0
  %102 = load double, double* %101, align 8
  %103 = fmul double %88, %102
  %104 = fadd double %100, %103
  br label %.thread

.loopexit:                                        ; preds = %0
  %105 = icmp sgt i32 %n, 5
  br i1 %105, label %106, label %.thread

106:                                              ; preds = %.loopexit
  call void @r_init(double* nonnull %1, i32 5, double 0.000000e+00) #4
  %107 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %108 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %109 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %.promoted5 = load double, double* %1, align 16
  %110 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 1, i64 0, i64 0
  %111 = load double, double* %110, align 8
  %112 = fmul double %107, %111
  %113 = fadd double %.promoted5, %112
  %114 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 2, i64 0, i64 0
  %115 = load double, double* %114, align 8
  %116 = fmul double %108, %115
  %117 = fadd double %113, %116
  %118 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 3, i64 0, i64 0
  %119 = load double, double* %118, align 8
  %120 = fmul double %109, %119
  %121 = fadd double %117, %120
  store double %121, double* %1, align 16
  %.promoted5.1 = load double, double* %21, align 8
  %122 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 1, i64 0, i64 1
  %123 = load double, double* %122, align 8
  %124 = fmul double %107, %123
  %125 = fadd double %.promoted5.1, %124
  %126 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 2, i64 0, i64 1
  %127 = load double, double* %126, align 8
  %128 = fmul double %108, %127
  %129 = fadd double %125, %128
  %130 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 3, i64 0, i64 1
  %131 = load double, double* %130, align 8
  %132 = fmul double %109, %131
  %133 = fadd double %129, %132
  store double %133, double* %21, align 8
  %.promoted5.2 = load double, double* %36, align 16
  %134 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 1, i64 0, i64 2
  %135 = load double, double* %134, align 8
  %136 = fmul double %107, %135
  %137 = fadd double %.promoted5.2, %136
  %138 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 2, i64 0, i64 2
  %139 = load double, double* %138, align 8
  %140 = fmul double %108, %139
  %141 = fadd double %137, %140
  %142 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 3, i64 0, i64 2
  %143 = load double, double* %142, align 8
  %144 = fmul double %109, %143
  %145 = fadd double %141, %144
  store double %145, double* %36, align 16
  %.promoted5.3 = load double, double* %51, align 8
  %146 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 1, i64 0, i64 3
  %147 = load double, double* %146, align 8
  %148 = fmul double %107, %147
  %149 = fadd double %.promoted5.3, %148
  %150 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 2, i64 0, i64 3
  %151 = load double, double* %150, align 8
  %152 = fmul double %108, %151
  %153 = fadd double %149, %152
  %154 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 3, i64 0, i64 3
  %155 = load double, double* %154, align 8
  %156 = fmul double %109, %155
  %157 = fadd double %153, %156
  store double %157, double* %51, align 8
  %.promoted5.4 = load double, double* %66, align 16
  %158 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 1, i64 0, i64 4
  %159 = load double, double* %158, align 8
  %160 = fmul double %107, %159
  %161 = fadd double %.promoted5.4, %160
  %162 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 2, i64 0, i64 4
  %163 = load double, double* %162, align 8
  %164 = fmul double %108, %163
  %165 = fadd double %161, %164
  %166 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 3, i64 0, i64 4
  %167 = load double, double* %166, align 8
  %168 = fmul double %109, %167
  %169 = fadd double %165, %168
  store double %169, double* %66, align 16
  %170 = load double, double* %1, align 16
  %171 = fadd double %91, %170
  %172 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %173 = load double, double* %21, align 8
  %174 = fmul double %172, %173
  %175 = fadd double %171, %174
  %176 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %177 = load double, double* %36, align 16
  %178 = fmul double %176, %177
  %179 = fadd double %175, %178
  %180 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %181 = load double, double* %51, align 8
  %182 = fmul double %180, %181
  %183 = fadd double %179, %182
  %184 = icmp eq i32 %n, 7
  br i1 %184, label %.thread.loopexit, label %.thread

.thread.loopexit:                                 ; preds = %106
  call void @r_init(double* nonnull %1, i32 5, double 0.000000e+00) #4
  %185 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %186 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %187 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %.promoted = load double, double* %21, align 8
  %188 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 1, i64 1, i64 0
  %189 = load double, double* %188, align 8
  %190 = fmul double %185, %189
  %191 = fadd double %.promoted, %190
  %192 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 2, i64 1, i64 0
  %193 = load double, double* %192, align 8
  %194 = fmul double %186, %193
  %195 = fadd double %191, %194
  %196 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 3, i64 1, i64 0
  %197 = load double, double* %196, align 8
  %198 = fmul double %187, %197
  %199 = fadd double %195, %198
  store double %199, double* %21, align 8
  %.promoted.1 = load double, double* %36, align 16
  %200 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 1, i64 2, i64 0
  %201 = load double, double* %200, align 8
  %202 = fmul double %185, %201
  %203 = fadd double %.promoted.1, %202
  %204 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 2, i64 2, i64 0
  %205 = load double, double* %204, align 8
  %206 = fmul double %186, %205
  %207 = fadd double %203, %206
  %208 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 3, i64 2, i64 0
  %209 = load double, double* %208, align 8
  %210 = fmul double %187, %209
  %211 = fadd double %207, %210
  store double %211, double* %36, align 16
  %.promoted.2 = load double, double* %51, align 8
  %212 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 1, i64 3, i64 0
  %213 = load double, double* %212, align 8
  %214 = fmul double %185, %213
  %215 = fadd double %.promoted.2, %214
  %216 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 2, i64 3, i64 0
  %217 = load double, double* %216, align 8
  %218 = fmul double %186, %217
  %219 = fadd double %215, %218
  %220 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 3, i64 3, i64 0
  %221 = load double, double* %220, align 8
  %222 = fmul double %187, %221
  %223 = fadd double %219, %222
  store double %223, double* %51, align 8
  %224 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %225 = load double, double* %21, align 8
  %226 = fmul double %224, %225
  %227 = fadd double %183, %226
  %228 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %229 = load double, double* %36, align 16
  %230 = fmul double %228, %229
  %231 = fadd double %227, %230
  %232 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %233 = fmul double %232, %223
  %234 = fadd double %231, %233
  br label %.thread

.thread:                                          ; preds = %.thread.loopexit, %106, %.loopexit, %.loopexit.thread
  %tmp.6 = phi double [ %183, %106 ], [ %91, %.loopexit ], [ %234, %.thread.loopexit ], [ %104, %.loopexit.thread ]
  store double %tmp.6, double* %tmor, align 8
  ret void
}

; Function Attrs: nounwind uwtable
define void @transf_nc([5 x double]* nocapture readonly %tmor, [5 x double]* nocapture %tx) local_unnamed_addr #0 {
  %tmp = alloca [5 x [5 x double]], align 16
  %1 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 0, i64 0
  call void @r_init(double* nonnull %1, i32 25, double 0.000000e+00) #4
  %2 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %3 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 0), align 8
  %4 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 0), align 16
  %5 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 0), align 8
  %6 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 0), align 16
  %7 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %8 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 1), align 8
  %9 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 1), align 8
  %10 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 1), align 8
  %11 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 1), align 8
  %12 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %13 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 2), align 8
  %14 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 2), align 16
  %15 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 2), align 8
  %16 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 2), align 16
  br label %17

17:                                               ; preds = %18, %0
  %indvars.iv17 = phi i64 [ %indvars.iv.next18, %18 ], [ 0, %0 ]
  %exitcond19 = icmp eq i64 %indvars.iv17, 5
  br i1 %exitcond19, label %.preheader1, label %18

18:                                               ; preds = %17
  %19 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv17, i64 0
  %20 = bitcast double* %19 to i64*
  %21 = load i64, i64* %20, align 8
  %22 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 %indvars.iv17
  %23 = bitcast [5 x double]* %22 to i64*
  store i64 %21, i64* %23, align 8
  %24 = bitcast i64 %21 to double
  %25 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv17, i64 1
  %26 = load double, double* %25, align 8
  %27 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv17, i64 2
  %28 = load double, double* %27, align 8
  %29 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv17, i64 3
  %30 = load double, double* %29, align 8
  %31 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv17, i64 4
  %32 = load double, double* %31, align 8
  %33 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 %indvars.iv17, i64 1
  %.promoted = load double, double* %33, align 8
  %34 = fmul double %2, %24
  %35 = fadd double %.promoted, %34
  %36 = fmul double %3, %26
  %37 = fadd double %35, %36
  %38 = fmul double %4, %28
  %39 = fadd double %37, %38
  %40 = fmul double %5, %30
  %41 = fadd double %39, %40
  %42 = fmul double %6, %32
  %43 = fadd double %41, %42
  store double %43, double* %33, align 8
  %44 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 %indvars.iv17, i64 2
  %.promoted.1 = load double, double* %44, align 8
  %45 = fmul double %7, %24
  %46 = fadd double %.promoted.1, %45
  %47 = fmul double %8, %26
  %48 = fadd double %46, %47
  %49 = fmul double %9, %28
  %50 = fadd double %48, %49
  %51 = fmul double %10, %30
  %52 = fadd double %50, %51
  %53 = fmul double %11, %32
  %54 = fadd double %52, %53
  store double %54, double* %44, align 8
  %55 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 %indvars.iv17, i64 3
  %.promoted.2 = load double, double* %55, align 8
  %56 = fmul double %12, %24
  %57 = fadd double %.promoted.2, %56
  %58 = fmul double %13, %26
  %59 = fadd double %57, %58
  %60 = fmul double %14, %28
  %61 = fadd double %59, %60
  %62 = fmul double %15, %30
  %63 = fadd double %61, %62
  %64 = fmul double %16, %32
  %65 = fadd double %63, %64
  store double %65, double* %55, align 8
  %indvars.iv.next18 = add nuw nsw i64 %indvars.iv17, 1
  br label %17

.preheader1:                                      ; preds = %66, %17
  %indvars.iv6 = phi i64 [ %indvars.iv.next7, %66 ], [ 0, %17 ]
  %exitcond8 = icmp eq i64 %indvars.iv6, 5
  br i1 %exitcond8, label %131, label %66

66:                                               ; preds = %.preheader1
  %67 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 0, i64 %indvars.iv6
  %68 = load double, double* %67, align 8
  %69 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 0, i64 %indvars.iv6
  %70 = load double, double* %69, align 8
  %71 = fadd double %68, %70
  store double %71, double* %67, align 8
  %72 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 1, i64 %indvars.iv6
  %73 = load double, double* %72, align 8
  %74 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 2, i64 %indvars.iv6
  %75 = load double, double* %74, align 8
  %76 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 3, i64 %indvars.iv6
  %77 = load double, double* %76, align 8
  %78 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 4, i64 %indvars.iv6
  %79 = load double, double* %78, align 8
  %80 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 1, i64 %indvars.iv6
  %81 = load double, double* %80, align 8
  %82 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %83 = fmul double %82, %70
  %84 = fadd double %81, %83
  store double %84, double* %80, align 8
  %85 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 0), align 8
  %86 = fmul double %85, %73
  %87 = fadd double %84, %86
  store double %87, double* %80, align 8
  %88 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 0), align 16
  %89 = fmul double %88, %75
  %90 = fadd double %87, %89
  store double %90, double* %80, align 8
  %91 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 0), align 8
  %92 = fmul double %91, %77
  %93 = fadd double %90, %92
  store double %93, double* %80, align 8
  %94 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 0), align 16
  %95 = fmul double %94, %79
  %96 = fadd double %93, %95
  store double %96, double* %80, align 8
  %97 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 2, i64 %indvars.iv6
  %98 = load double, double* %97, align 8
  %99 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %100 = fmul double %99, %70
  %101 = fadd double %98, %100
  store double %101, double* %97, align 8
  %102 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 1), align 8
  %103 = fmul double %102, %73
  %104 = fadd double %101, %103
  store double %104, double* %97, align 8
  %105 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 1), align 8
  %106 = fmul double %105, %75
  %107 = fadd double %104, %106
  store double %107, double* %97, align 8
  %108 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 1), align 8
  %109 = fmul double %108, %77
  %110 = fadd double %107, %109
  store double %110, double* %97, align 8
  %111 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 1), align 8
  %112 = fmul double %111, %79
  %113 = fadd double %110, %112
  store double %113, double* %97, align 8
  %114 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 3, i64 %indvars.iv6
  %115 = load double, double* %114, align 8
  %116 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %117 = fmul double %116, %70
  %118 = fadd double %115, %117
  store double %118, double* %114, align 8
  %119 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 2), align 8
  %120 = fmul double %119, %73
  %121 = fadd double %118, %120
  store double %121, double* %114, align 8
  %122 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 2), align 16
  %123 = fmul double %122, %75
  %124 = fadd double %121, %123
  store double %124, double* %114, align 8
  %125 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 2), align 8
  %126 = fmul double %125, %77
  %127 = fadd double %124, %126
  store double %127, double* %114, align 8
  %128 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 2), align 16
  %129 = fmul double %128, %79
  %130 = fadd double %127, %129
  store double %130, double* %114, align 8
  %indvars.iv.next7 = add nuw nsw i64 %indvars.iv6, 1
  br label %.preheader1

131:                                              ; preds = %.preheader1
  ret void
}

; Function Attrs: nounwind uwtable
define void @transfb_nc0([5 x double]* %tmor, [5 x [5 x double]]* nocapture readonly %tx) local_unnamed_addr #0 {
  %1 = getelementptr [5 x double], [5 x double]* %tmor, i64 0, i64 0
  tail call void @r_init(double* %1, i32 25, double 0.000000e+00) #4
  %2 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 1
  %3 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 2
  %4 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 3
  %5 = load double, double* %1, align 8
  %6 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %7 = load double, double* %2, align 8
  %8 = fmul double %6, %7
  %9 = fadd double %5, %8
  store double %9, double* %1, align 8
  %10 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %11 = load double, double* %3, align 8
  %12 = fmul double %10, %11
  %13 = fadd double %9, %12
  store double %13, double* %1, align 8
  %14 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %15 = load double, double* %4, align 8
  %16 = fmul double %14, %15
  %17 = fadd double %13, %16
  store double %17, double* %1, align 8
  %18 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 1
  %19 = load double, double* %18, align 8
  %20 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 0), align 8
  %21 = load double, double* %2, align 8
  %22 = fmul double %20, %21
  %23 = fadd double %19, %22
  store double %23, double* %18, align 8
  %24 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 1), align 8
  %25 = load double, double* %3, align 8
  %26 = fmul double %24, %25
  %27 = fadd double %23, %26
  store double %27, double* %18, align 8
  %28 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 2), align 8
  %29 = load double, double* %4, align 8
  %30 = fmul double %28, %29
  %31 = fadd double %27, %30
  store double %31, double* %18, align 8
  %32 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 2
  %33 = load double, double* %32, align 8
  %34 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 0), align 16
  %35 = load double, double* %2, align 8
  %36 = fmul double %34, %35
  %37 = fadd double %33, %36
  store double %37, double* %32, align 8
  %38 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 1), align 8
  %39 = load double, double* %3, align 8
  %40 = fmul double %38, %39
  %41 = fadd double %37, %40
  store double %41, double* %32, align 8
  %42 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 2), align 16
  %43 = load double, double* %4, align 8
  %44 = fmul double %42, %43
  %45 = fadd double %41, %44
  store double %45, double* %32, align 8
  %46 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 3
  %47 = load double, double* %46, align 8
  %48 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 0), align 8
  %49 = load double, double* %2, align 8
  %50 = fmul double %48, %49
  %51 = fadd double %47, %50
  store double %51, double* %46, align 8
  %52 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 1), align 8
  %53 = load double, double* %3, align 8
  %54 = fmul double %52, %53
  %55 = fadd double %51, %54
  store double %55, double* %46, align 8
  %56 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 2), align 8
  %57 = load double, double* %4, align 8
  %58 = fmul double %56, %57
  %59 = fadd double %55, %58
  store double %59, double* %46, align 8
  %60 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 4
  %61 = load double, double* %60, align 8
  %62 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 0), align 16
  %63 = load double, double* %2, align 8
  %64 = fmul double %62, %63
  %65 = fadd double %61, %64
  store double %65, double* %60, align 8
  %66 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 1), align 8
  %67 = load double, double* %3, align 8
  %68 = fmul double %66, %67
  %69 = fadd double %65, %68
  store double %69, double* %60, align 8
  %70 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 2), align 16
  %71 = load double, double* %4, align 8
  %72 = fmul double %70, %71
  %73 = fadd double %69, %72
  store double %73, double* %60, align 8
  ret void
}

; Function Attrs: nounwind uwtable
define void @transfb_nc2([5 x double]* %tmor, [5 x double]* nocapture readonly %tx) local_unnamed_addr #0 {
  %bottom = alloca [5 x double], align 16
  %temp = alloca [5 x [5 x double]], align 16
  %1 = getelementptr [5 x double], [5 x double]* %tmor, i64 0, i64 0
  tail call void @r_init(double* %1, i32 25, double 0.000000e+00) #4
  %2 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 0
  call void @r_init(double* nonnull %2, i32 25, double 0.000000e+00) #4
  %3 = bitcast [5 x double]* %tx to i64*
  %4 = load i64, i64* %3, align 8
  %5 = bitcast [5 x double]* %tmor to i64*
  store i64 %4, i64* %5, align 8
  %6 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %7 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %8 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %9 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 0), align 8
  %10 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 1), align 8
  %11 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 2), align 8
  %12 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 0), align 16
  %13 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 1), align 8
  %14 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 2), align 16
  %15 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 0), align 8
  %16 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 1), align 8
  %17 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 2), align 8
  %18 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 0), align 16
  %19 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 1), align 8
  %20 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 2), align 16
  br label %21

21:                                               ; preds = %.preheader5, %0
  %indvars.iv36 = phi i64 [ %indvars.iv.next37, %.preheader5 ], [ 0, %0 ]
  %exitcond38 = icmp eq i64 %indvars.iv36, 5
  br i1 %exitcond38, label %.preheader3.preheader, label %.preheader5

.preheader3.preheader:                            ; preds = %21
  %22 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 1
  %23 = load double, double* %22, align 8
  %24 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 1
  %25 = load double, double* %24, align 8
  %26 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 2
  %27 = load double, double* %26, align 16
  %28 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 2
  %29 = load double, double* %28, align 16
  %30 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 3
  %31 = load double, double* %30, align 8
  %32 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 3
  %33 = load double, double* %32, align 8
  %34 = load double, double* %1, align 8
  %35 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %36 = fmul double %35, %23
  %37 = fadd double %34, %36
  %38 = fmul double %35, %25
  %39 = fmul double %38, 5.000000e-01
  %40 = fadd double %37, %39
  store double %40, double* %1, align 8
  %41 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %42 = fmul double %41, %27
  %43 = fadd double %40, %42
  %44 = fmul double %41, %29
  %45 = fmul double %44, 5.000000e-01
  %46 = fadd double %43, %45
  store double %46, double* %1, align 8
  %47 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %48 = fmul double %47, %31
  %49 = fadd double %46, %48
  %50 = fmul double %47, %33
  %51 = fmul double %50, 5.000000e-01
  %52 = fadd double %49, %51
  store double %52, double* %1, align 8
  %53 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 1
  %54 = load double, double* %53, align 8
  %55 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 0), align 8
  %56 = fmul double %55, %23
  %57 = fadd double %54, %56
  %58 = fmul double %55, %25
  %59 = fmul double %58, 5.000000e-01
  %60 = fadd double %57, %59
  store double %60, double* %53, align 8
  %61 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 1), align 8
  %62 = fmul double %61, %27
  %63 = fadd double %60, %62
  %64 = fmul double %61, %29
  %65 = fmul double %64, 5.000000e-01
  %66 = fadd double %63, %65
  store double %66, double* %53, align 8
  %67 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 2), align 8
  %68 = fmul double %67, %31
  %69 = fadd double %66, %68
  %70 = fmul double %67, %33
  %71 = fmul double %70, 5.000000e-01
  %72 = fadd double %69, %71
  store double %72, double* %53, align 8
  %73 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 2
  %74 = load double, double* %73, align 8
  %75 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 0), align 16
  %76 = fmul double %75, %23
  %77 = fadd double %74, %76
  %78 = fmul double %75, %25
  %79 = fmul double %78, 5.000000e-01
  %80 = fadd double %77, %79
  store double %80, double* %73, align 8
  %81 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 1), align 8
  %82 = fmul double %81, %27
  %83 = fadd double %80, %82
  %84 = fmul double %81, %29
  %85 = fmul double %84, 5.000000e-01
  %86 = fadd double %83, %85
  store double %86, double* %73, align 8
  %87 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 2), align 16
  %88 = fmul double %87, %31
  %89 = fadd double %86, %88
  %90 = fmul double %87, %33
  %91 = fmul double %90, 5.000000e-01
  %92 = fadd double %89, %91
  store double %92, double* %73, align 8
  %93 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 3
  %94 = load double, double* %93, align 8
  %95 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 0), align 8
  %96 = fmul double %95, %23
  %97 = fadd double %94, %96
  %98 = fmul double %95, %25
  %99 = fmul double %98, 5.000000e-01
  %100 = fadd double %97, %99
  store double %100, double* %93, align 8
  %101 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 1), align 8
  %102 = fmul double %101, %27
  %103 = fadd double %100, %102
  %104 = fmul double %101, %29
  %105 = fmul double %104, 5.000000e-01
  %106 = fadd double %103, %105
  store double %106, double* %93, align 8
  %107 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 2), align 8
  %108 = fmul double %107, %31
  %109 = fadd double %106, %108
  %110 = fmul double %107, %33
  %111 = fmul double %110, 5.000000e-01
  %112 = fadd double %109, %111
  store double %112, double* %93, align 8
  %113 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 4
  %114 = load double, double* %113, align 8
  %115 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 0), align 16
  %116 = fmul double %115, %23
  %117 = fadd double %114, %116
  %118 = fmul double %115, %25
  %119 = fmul double %118, 5.000000e-01
  %120 = fadd double %117, %119
  store double %120, double* %113, align 8
  %121 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 1), align 8
  %122 = fmul double %121, %27
  %123 = fadd double %120, %122
  %124 = fmul double %121, %29
  %125 = fmul double %124, 5.000000e-01
  %126 = fadd double %123, %125
  store double %126, double* %113, align 8
  %127 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 2), align 16
  %128 = fmul double %127, %31
  %129 = fadd double %126, %128
  %130 = fmul double %127, %33
  %131 = fmul double %130, 5.000000e-01
  %132 = fadd double %129, %131
  store double %132, double* %113, align 8
  br label %.preheader1

.preheader5:                                      ; preds = %21
  %133 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 0, i64 %indvars.iv36
  %134 = bitcast double* %133 to i64*
  %135 = load i64, i64* %134, align 8
  %136 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 %indvars.iv36
  %137 = bitcast double* %136 to i64*
  store i64 %135, i64* %137, align 8
  %138 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 %indvars.iv36
  %139 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 1, i64 %indvars.iv36
  %140 = load double, double* %139, align 8
  %141 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 2, i64 %indvars.iv36
  %142 = load double, double* %141, align 8
  %143 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 3, i64 %indvars.iv36
  %144 = load double, double* %143, align 8
  %145 = fmul double %6, %140
  %146 = fadd double %145, 0.000000e+00
  %147 = fmul double %7, %142
  %148 = fadd double %146, %147
  %149 = fmul double %8, %144
  %150 = fadd double %148, %149
  store double %150, double* %138, align 8
  %151 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 1, i64 %indvars.iv36
  %.promoted6 = load double, double* %151, align 8
  %152 = fmul double %9, %140
  %153 = fadd double %.promoted6, %152
  %154 = fmul double %10, %142
  %155 = fadd double %153, %154
  %156 = fmul double %11, %144
  %157 = fadd double %155, %156
  store double %157, double* %151, align 8
  %158 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 2, i64 %indvars.iv36
  %.promoted6.1 = load double, double* %158, align 8
  %159 = fmul double %12, %140
  %160 = fadd double %.promoted6.1, %159
  %161 = fmul double %13, %142
  %162 = fadd double %160, %161
  %163 = fmul double %14, %144
  %164 = fadd double %162, %163
  store double %164, double* %158, align 8
  %165 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 3, i64 %indvars.iv36
  %.promoted6.2 = load double, double* %165, align 8
  %166 = fmul double %15, %140
  %167 = fadd double %.promoted6.2, %166
  %168 = fmul double %16, %142
  %169 = fadd double %167, %168
  %170 = fmul double %17, %144
  %171 = fadd double %169, %170
  store double %171, double* %165, align 8
  %172 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 4, i64 %indvars.iv36
  %.promoted6.3 = load double, double* %172, align 8
  %173 = fmul double %18, %140
  %174 = fadd double %.promoted6.3, %173
  %175 = fmul double %19, %142
  %176 = fadd double %174, %175
  %177 = fmul double %20, %144
  %178 = fadd double %176, %177
  store double %178, double* %172, align 8
  %indvars.iv.next37 = add nuw nsw i64 %indvars.iv36, 1
  br label %21

.preheader1:                                      ; preds = %179, %.preheader3.preheader
  %indvars.iv12 = phi i64 [ %indvars.iv.next13, %179 ], [ 1, %.preheader3.preheader ]
  %exitcond14 = icmp eq i64 %indvars.iv12, 5
  br i1 %exitcond14, label %244, label %179

179:                                              ; preds = %.preheader1
  %180 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv12, i64 0
  %181 = load double, double* %180, align 8
  %182 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv12, i64 0
  %183 = load double, double* %182, align 8
  %184 = fadd double %181, %183
  store double %184, double* %180, align 8
  %185 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv12, i64 1
  %186 = load double, double* %185, align 8
  %187 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv12, i64 2
  %188 = load double, double* %187, align 8
  %189 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv12, i64 3
  %190 = load double, double* %189, align 8
  %191 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %192 = fmul double %191, %186
  %193 = fadd double %184, %192
  store double %193, double* %180, align 8
  %194 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %195 = fmul double %194, %188
  %196 = fadd double %193, %195
  store double %196, double* %180, align 8
  %197 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %198 = fmul double %197, %190
  %199 = fadd double %196, %198
  store double %199, double* %180, align 8
  %200 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv12, i64 1
  %201 = load double, double* %200, align 8
  %202 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 0), align 8
  %203 = fmul double %202, %186
  %204 = fadd double %201, %203
  store double %204, double* %200, align 8
  %205 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 1), align 8
  %206 = fmul double %205, %188
  %207 = fadd double %204, %206
  store double %207, double* %200, align 8
  %208 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 2), align 8
  %209 = fmul double %208, %190
  %210 = fadd double %207, %209
  store double %210, double* %200, align 8
  %211 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv12, i64 2
  %212 = load double, double* %211, align 8
  %213 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 0), align 16
  %214 = fmul double %213, %186
  %215 = fadd double %212, %214
  store double %215, double* %211, align 8
  %216 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 1), align 8
  %217 = fmul double %216, %188
  %218 = fadd double %215, %217
  store double %218, double* %211, align 8
  %219 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 2), align 16
  %220 = fmul double %219, %190
  %221 = fadd double %218, %220
  store double %221, double* %211, align 8
  %222 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv12, i64 3
  %223 = load double, double* %222, align 8
  %224 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 0), align 8
  %225 = fmul double %224, %186
  %226 = fadd double %223, %225
  store double %226, double* %222, align 8
  %227 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 1), align 8
  %228 = fmul double %227, %188
  %229 = fadd double %226, %228
  store double %229, double* %222, align 8
  %230 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 2), align 8
  %231 = fmul double %230, %190
  %232 = fadd double %229, %231
  store double %232, double* %222, align 8
  %233 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv12, i64 4
  %234 = load double, double* %233, align 8
  %235 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 0), align 16
  %236 = fmul double %235, %186
  %237 = fadd double %234, %236
  store double %237, double* %233, align 8
  %238 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 1), align 8
  %239 = fmul double %238, %188
  %240 = fadd double %237, %239
  store double %240, double* %233, align 8
  %241 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 2), align 16
  %242 = fmul double %241, %190
  %243 = fadd double %240, %242
  store double %243, double* %233, align 8
  %indvars.iv.next13 = add nuw nsw i64 %indvars.iv12, 1
  br label %.preheader1

244:                                              ; preds = %.preheader1
  ret void
}

; Function Attrs: nounwind uwtable
define void @transfb_nc1([5 x double]* %tmor, [5 x double]* nocapture readonly %tx) local_unnamed_addr #0 {
  %bottom = alloca [5 x double], align 16
  %temp = alloca [5 x [5 x double]], align 16
  %1 = getelementptr [5 x double], [5 x double]* %tmor, i64 0, i64 0
  tail call void @r_init(double* %1, i32 25, double 0.000000e+00) #4
  %2 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 0
  call void @r_init(double* nonnull %2, i32 25, double 0.000000e+00) #4
  %3 = bitcast [5 x double]* %tx to i64*
  %4 = load i64, i64* %3, align 8
  %5 = bitcast [5 x double]* %tmor to i64*
  store i64 %4, i64* %5, align 8
  %6 = bitcast i64 %4 to double
  %7 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %8 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %9 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %10 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 0), align 8
  %11 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 1), align 8
  %12 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 2), align 8
  %13 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 0), align 16
  %14 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 1), align 8
  %15 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 2), align 16
  %16 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 0), align 8
  %17 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 1), align 8
  %18 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 2), align 8
  %19 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 0), align 16
  %20 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 1), align 8
  %21 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 2), align 16
  br label %22

22:                                               ; preds = %.preheader4, %0
  %indvars.iv35 = phi i64 [ %indvars.iv.next36, %.preheader4 ], [ 0, %0 ]
  %exitcond37 = icmp eq i64 %indvars.iv35, 5
  br i1 %exitcond37, label %.preheader1.preheader, label %.preheader4

.preheader4:                                      ; preds = %22
  %23 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 0, i64 %indvars.iv35
  %24 = bitcast double* %23 to i64*
  %25 = load i64, i64* %24, align 8
  %26 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 %indvars.iv35
  %27 = bitcast double* %26 to i64*
  store i64 %25, i64* %27, align 8
  %28 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 %indvars.iv35
  %29 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 1, i64 %indvars.iv35
  %30 = load double, double* %29, align 8
  %31 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 2, i64 %indvars.iv35
  %32 = load double, double* %31, align 8
  %33 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 3, i64 %indvars.iv35
  %34 = load double, double* %33, align 8
  %35 = fmul double %7, %30
  %36 = fadd double %35, 0.000000e+00
  %37 = fmul double %8, %32
  %38 = fadd double %36, %37
  %39 = fmul double %9, %34
  %40 = fadd double %38, %39
  store double %40, double* %28, align 8
  %41 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 1, i64 %indvars.iv35
  %.promoted5 = load double, double* %41, align 8
  %42 = fmul double %10, %30
  %43 = fadd double %.promoted5, %42
  %44 = fmul double %11, %32
  %45 = fadd double %43, %44
  %46 = fmul double %12, %34
  %47 = fadd double %45, %46
  store double %47, double* %41, align 8
  %48 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 2, i64 %indvars.iv35
  %.promoted5.1 = load double, double* %48, align 8
  %49 = fmul double %13, %30
  %50 = fadd double %.promoted5.1, %49
  %51 = fmul double %14, %32
  %52 = fadd double %50, %51
  %53 = fmul double %15, %34
  %54 = fadd double %52, %53
  store double %54, double* %48, align 8
  %55 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 3, i64 %indvars.iv35
  %.promoted5.2 = load double, double* %55, align 8
  %56 = fmul double %16, %30
  %57 = fadd double %.promoted5.2, %56
  %58 = fmul double %17, %32
  %59 = fadd double %57, %58
  %60 = fmul double %18, %34
  %61 = fadd double %59, %60
  store double %61, double* %55, align 8
  %62 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 4, i64 %indvars.iv35
  %.promoted5.3 = load double, double* %62, align 8
  %63 = fmul double %19, %30
  %64 = fadd double %.promoted5.3, %63
  %65 = fmul double %20, %32
  %66 = fadd double %64, %65
  %67 = fmul double %21, %34
  %68 = fadd double %66, %67
  store double %68, double* %62, align 8
  %indvars.iv.next36 = add nuw nsw i64 %indvars.iv35, 1
  br label %22

.preheader1.preheader:                            ; preds = %22
  %69 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 0
  %70 = load double, double* %69, align 16
  %71 = fadd double %70, %6
  store double %71, double* %1, align 8
  %72 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 1
  %73 = load double, double* %72, align 8
  %74 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 1
  %75 = load double, double* %74, align 8
  %76 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 2
  %77 = load double, double* %76, align 16
  %78 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 2
  %79 = load double, double* %78, align 16
  %80 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 3
  %81 = load double, double* %80, align 8
  %82 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 3
  %83 = load double, double* %82, align 8
  %84 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %85 = fmul double %84, %73
  %86 = fadd double %71, %85
  %87 = fmul double %84, %75
  %88 = fadd double %86, %87
  store double %88, double* %1, align 8
  %89 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %90 = fmul double %89, %77
  %91 = fadd double %88, %90
  %92 = fmul double %89, %79
  %93 = fadd double %91, %92
  store double %93, double* %1, align 8
  %94 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %95 = fmul double %94, %81
  %96 = fadd double %93, %95
  %97 = fmul double %94, %83
  %98 = fadd double %96, %97
  store double %98, double* %1, align 8
  %99 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 1
  %100 = load double, double* %99, align 8
  %101 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 0), align 8
  %102 = fmul double %101, %73
  %103 = fadd double %100, %102
  %104 = fmul double %101, %75
  %105 = fadd double %103, %104
  store double %105, double* %99, align 8
  %106 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 1), align 8
  %107 = fmul double %106, %77
  %108 = fadd double %105, %107
  %109 = fmul double %106, %79
  %110 = fadd double %108, %109
  store double %110, double* %99, align 8
  %111 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 2), align 8
  %112 = fmul double %111, %81
  %113 = fadd double %110, %112
  %114 = fmul double %111, %83
  %115 = fadd double %113, %114
  store double %115, double* %99, align 8
  %116 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 2
  %117 = load double, double* %116, align 8
  %118 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 0), align 16
  %119 = fmul double %118, %73
  %120 = fadd double %117, %119
  %121 = fmul double %118, %75
  %122 = fadd double %120, %121
  store double %122, double* %116, align 8
  %123 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 1), align 8
  %124 = fmul double %123, %77
  %125 = fadd double %122, %124
  %126 = fmul double %123, %79
  %127 = fadd double %125, %126
  store double %127, double* %116, align 8
  %128 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 2), align 16
  %129 = fmul double %128, %81
  %130 = fadd double %127, %129
  %131 = fmul double %128, %83
  %132 = fadd double %130, %131
  store double %132, double* %116, align 8
  %133 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 3
  %134 = load double, double* %133, align 8
  %135 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 0), align 8
  %136 = fmul double %135, %73
  %137 = fadd double %134, %136
  %138 = fmul double %135, %75
  %139 = fadd double %137, %138
  store double %139, double* %133, align 8
  %140 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 1), align 8
  %141 = fmul double %140, %77
  %142 = fadd double %139, %141
  %143 = fmul double %140, %79
  %144 = fadd double %142, %143
  store double %144, double* %133, align 8
  %145 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 2), align 8
  %146 = fmul double %145, %81
  %147 = fadd double %144, %146
  %148 = fmul double %145, %83
  %149 = fadd double %147, %148
  store double %149, double* %133, align 8
  %150 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 4
  %151 = load double, double* %150, align 8
  %152 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 0), align 16
  %153 = fmul double %152, %73
  %154 = fadd double %151, %153
  %155 = fmul double %152, %75
  %156 = fadd double %154, %155
  store double %156, double* %150, align 8
  %157 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 1), align 8
  %158 = fmul double %157, %77
  %159 = fadd double %156, %158
  %160 = fmul double %157, %79
  %161 = fadd double %159, %160
  store double %161, double* %150, align 8
  %162 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 2), align 16
  %163 = fmul double %162, %81
  %164 = fadd double %161, %163
  %165 = fmul double %162, %83
  %166 = fadd double %164, %165
  store double %166, double* %150, align 8
  br label %.preheader1

.preheader1:                                      ; preds = %167, %.preheader1.preheader
  %indvars.iv11 = phi i64 [ %indvars.iv.next12, %167 ], [ 1, %.preheader1.preheader ]
  %exitcond13 = icmp eq i64 %indvars.iv11, 5
  br i1 %exitcond13, label %232, label %167

167:                                              ; preds = %.preheader1
  %168 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv11, i64 0
  %169 = load double, double* %168, align 8
  %170 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv11, i64 0
  %171 = load double, double* %170, align 8
  %172 = fadd double %169, %171
  store double %172, double* %168, align 8
  %173 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv11, i64 1
  %174 = load double, double* %173, align 8
  %175 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv11, i64 2
  %176 = load double, double* %175, align 8
  %177 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv11, i64 3
  %178 = load double, double* %177, align 8
  %179 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 0), align 16
  %180 = fmul double %179, %174
  %181 = fadd double %172, %180
  store double %181, double* %168, align 8
  %182 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 1), align 8
  %183 = fmul double %182, %176
  %184 = fadd double %181, %183
  store double %184, double* %168, align 8
  %185 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 2), align 16
  %186 = fmul double %185, %178
  %187 = fadd double %184, %186
  store double %187, double* %168, align 8
  %188 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv11, i64 1
  %189 = load double, double* %188, align 8
  %190 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 0), align 8
  %191 = fmul double %190, %174
  %192 = fadd double %189, %191
  store double %192, double* %188, align 8
  %193 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 1), align 8
  %194 = fmul double %193, %176
  %195 = fadd double %192, %194
  store double %195, double* %188, align 8
  %196 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 1, i64 2), align 8
  %197 = fmul double %196, %178
  %198 = fadd double %195, %197
  store double %198, double* %188, align 8
  %199 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv11, i64 2
  %200 = load double, double* %199, align 8
  %201 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 0), align 16
  %202 = fmul double %201, %174
  %203 = fadd double %200, %202
  store double %203, double* %199, align 8
  %204 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 1), align 8
  %205 = fmul double %204, %176
  %206 = fadd double %203, %205
  store double %206, double* %199, align 8
  %207 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 2, i64 2), align 16
  %208 = fmul double %207, %178
  %209 = fadd double %206, %208
  store double %209, double* %199, align 8
  %210 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv11, i64 3
  %211 = load double, double* %210, align 8
  %212 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 0), align 8
  %213 = fmul double %212, %174
  %214 = fadd double %211, %213
  store double %214, double* %210, align 8
  %215 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 1), align 8
  %216 = fmul double %215, %176
  %217 = fadd double %214, %216
  store double %217, double* %210, align 8
  %218 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 3, i64 2), align 8
  %219 = fmul double %218, %178
  %220 = fadd double %217, %219
  store double %220, double* %210, align 8
  %221 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv11, i64 4
  %222 = load double, double* %221, align 8
  %223 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 0), align 16
  %224 = fmul double %223, %174
  %225 = fadd double %222, %224
  store double %225, double* %221, align 8
  %226 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 1), align 8
  %227 = fmul double %226, %176
  %228 = fadd double %225, %227
  store double %228, double* %221, align 8
  %229 = load double, double* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 4, i64 2), align 16
  %230 = fmul double %229, %178
  %231 = fadd double %228, %230
  store double %231, double* %221, align 8
  %indvars.iv.next12 = add nuw nsw i64 %indvars.iv11, 1
  br label %.preheader1

232:                                              ; preds = %.preheader1
  ret void
}

; Function Attrs: nounwind uwtable
define void @transfb_c(double* nocapture readonly %tx) local_unnamed_addr #0 {
  %1 = load i32, i32* @nmor, align 4
  tail call void @r_init(double* getelementptr inbounds ([334600 x double], [334600 x double]* @tmort, i64 0, i64 0), i32 %1, double 0.000000e+00) #4
  %2 = load i32, i32* @nelt, align 4
  %3 = sext i32 %2 to i64
  br label %4

4:                                                ; preds = %314, %0
  %indvars.iv46 = phi i64 [ %indvars.iv.next47, %314 ], [ 0, %0 ]
  %5 = icmp slt i64 %indvars.iv46, %3
  br i1 %5, label %.preheader8, label %315

.preheader8:                                      ; preds = %.loopexit, %4
  %indvars.iv43 = phi i64 [ %indvars.iv.next44, %.loopexit ], [ 0, %4 ]
  %exitcond45 = icmp eq i64 %indvars.iv43, 6
  br i1 %exitcond45, label %314, label %6

6:                                                ; preds = %.preheader8
  %7 = getelementptr inbounds [8800 x [6 x i32]], [8800 x [6 x i32]]* @cbc, i64 0, i64 %indvars.iv46, i64 %indvars.iv43
  %8 = load i32, i32* %7, align 4
  %9 = icmp eq i32 %8, 3
  br i1 %9, label %.loopexit, label %10

10:                                               ; preds = %6
  %11 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0
  %12 = load i32, i32* %11, align 4
  %13 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 4
  %14 = load i32, i32* %13, align 4
  %15 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 4, i64 0
  %16 = load i32, i32* %15, align 4
  %17 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 4, i64 4
  %18 = load i32, i32* %17, align 4
  %19 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 0, i64 0
  %20 = load i32, i32* %19, align 16
  %21 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 0, i64 0, i64 4
  %22 = load i32, i32* %21, align 8
  %23 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 1, i64 4, i64 0
  %24 = load i32, i32* %23, align 4
  %25 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 1, i64 4, i64 4
  %26 = load i32, i32* %25, align 4
  %27 = sext i32 %20 to i64
  %28 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %27
  %29 = load double, double* %28, align 8
  %30 = sext i32 %12 to i64
  %31 = getelementptr inbounds double, double* %tx, i64 %30
  %32 = load double, double* %31, align 8
  %33 = fmul double %32, 0x3FD5555555555555
  %34 = fadd double %29, %33
  store double %34, double* %28, align 8
  %35 = sext i32 %22 to i64
  %36 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %35
  %37 = load double, double* %36, align 8
  %38 = sext i32 %14 to i64
  %39 = getelementptr inbounds double, double* %tx, i64 %38
  %40 = load double, double* %39, align 8
  %41 = fmul double %40, 0x3FD5555555555555
  %42 = fadd double %37, %41
  store double %42, double* %36, align 8
  %43 = sext i32 %24 to i64
  %44 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %43
  %45 = load double, double* %44, align 8
  %46 = sext i32 %16 to i64
  %47 = getelementptr inbounds double, double* %tx, i64 %46
  %48 = load double, double* %47, align 8
  %49 = fmul double %48, 0x3FD5555555555555
  %50 = fadd double %45, %49
  store double %50, double* %44, align 8
  %51 = sext i32 %26 to i64
  %52 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %51
  %53 = load double, double* %52, align 8
  %54 = sext i32 %18 to i64
  %55 = getelementptr inbounds double, double* %tx, i64 %54
  %56 = load double, double* %55, align 8
  %57 = fmul double %56, 0x3FD5555555555555
  %58 = fadd double %53, %57
  store double %58, double* %52, align 8
  %59 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 1
  %60 = load i32, i32* %59, align 4
  %61 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 1, i64 1
  %62 = load i32, i32* %61, align 4
  %63 = sext i32 %62 to i64
  %64 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %63
  %65 = load double, double* %64, align 8
  %66 = sext i32 %60 to i64
  %67 = getelementptr inbounds double, double* %tx, i64 %66
  %68 = load double, double* %67, align 8
  %69 = fadd double %65, %68
  store double %69, double* %64, align 8
  %70 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 2
  %71 = load i32, i32* %70, align 4
  %72 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 1, i64 2
  %73 = load i32, i32* %72, align 4
  %74 = sext i32 %73 to i64
  %75 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %74
  %76 = load double, double* %75, align 8
  %77 = sext i32 %71 to i64
  %78 = getelementptr inbounds double, double* %tx, i64 %77
  %79 = load double, double* %78, align 8
  %80 = fadd double %76, %79
  store double %80, double* %75, align 8
  %81 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 3
  %82 = load i32, i32* %81, align 4
  %83 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 1, i64 3
  %84 = load i32, i32* %83, align 4
  %85 = sext i32 %84 to i64
  %86 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %85
  %87 = load double, double* %86, align 8
  %88 = sext i32 %82 to i64
  %89 = getelementptr inbounds double, double* %tx, i64 %88
  %90 = load double, double* %89, align 8
  %91 = fadd double %87, %90
  store double %91, double* %86, align 8
  %92 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 2, i64 1
  %93 = load i32, i32* %92, align 4
  %94 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 2, i64 1
  %95 = load i32, i32* %94, align 4
  %96 = sext i32 %95 to i64
  %97 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %96
  %98 = load double, double* %97, align 8
  %99 = sext i32 %93 to i64
  %100 = getelementptr inbounds double, double* %tx, i64 %99
  %101 = load double, double* %100, align 8
  %102 = fadd double %98, %101
  store double %102, double* %97, align 8
  %103 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 2, i64 2
  %104 = load i32, i32* %103, align 4
  %105 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 2, i64 2
  %106 = load i32, i32* %105, align 8
  %107 = sext i32 %106 to i64
  %108 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %107
  %109 = load double, double* %108, align 8
  %110 = sext i32 %104 to i64
  %111 = getelementptr inbounds double, double* %tx, i64 %110
  %112 = load double, double* %111, align 8
  %113 = fadd double %109, %112
  store double %113, double* %108, align 8
  %114 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 2, i64 3
  %115 = load i32, i32* %114, align 4
  %116 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 2, i64 3
  %117 = load i32, i32* %116, align 4
  %118 = sext i32 %117 to i64
  %119 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %118
  %120 = load double, double* %119, align 8
  %121 = sext i32 %115 to i64
  %122 = getelementptr inbounds double, double* %tx, i64 %121
  %123 = load double, double* %122, align 8
  %124 = fadd double %120, %123
  store double %124, double* %119, align 8
  %125 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 3, i64 1
  %126 = load i32, i32* %125, align 4
  %127 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 3, i64 1
  %128 = load i32, i32* %127, align 4
  %129 = sext i32 %128 to i64
  %130 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %129
  %131 = load double, double* %130, align 8
  %132 = sext i32 %126 to i64
  %133 = getelementptr inbounds double, double* %tx, i64 %132
  %134 = load double, double* %133, align 8
  %135 = fadd double %131, %134
  store double %135, double* %130, align 8
  %136 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 3, i64 2
  %137 = load i32, i32* %136, align 4
  %138 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 3, i64 2
  %139 = load i32, i32* %138, align 4
  %140 = sext i32 %139 to i64
  %141 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %140
  %142 = load double, double* %141, align 8
  %143 = sext i32 %137 to i64
  %144 = getelementptr inbounds double, double* %tx, i64 %143
  %145 = load double, double* %144, align 8
  %146 = fadd double %142, %145
  store double %146, double* %141, align 8
  %147 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 3, i64 3
  %148 = load i32, i32* %147, align 4
  %149 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 3, i64 3
  %150 = load i32, i32* %149, align 4
  %151 = sext i32 %150 to i64
  %152 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %151
  %153 = load double, double* %152, align 8
  %154 = sext i32 %148 to i64
  %155 = getelementptr inbounds double, double* %tx, i64 %154
  %156 = load double, double* %155, align 8
  %157 = fadd double %153, %156
  store double %157, double* %152, align 8
  %158 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 0, i64 4
  %159 = load i32, i32* %158, align 16
  %160 = icmp eq i32 %159, -1
  br i1 %160, label %.loopexit7.loopexit, label %.loopexit7

.loopexit7.loopexit:                              ; preds = %10
  %161 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 1
  %162 = load i32, i32* %161, align 4
  %163 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 0, i64 1
  %164 = load i32, i32* %163, align 4
  %165 = sext i32 %164 to i64
  %166 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %165
  %167 = load double, double* %166, align 8
  %168 = sext i32 %162 to i64
  %169 = getelementptr inbounds double, double* %tx, i64 %168
  %170 = load double, double* %169, align 8
  %171 = fmul double %170, 5.000000e-01
  %172 = fadd double %167, %171
  store double %172, double* %166, align 8
  %173 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 2
  %174 = load i32, i32* %173, align 4
  %175 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 0, i64 2
  %176 = load i32, i32* %175, align 8
  %177 = sext i32 %176 to i64
  %178 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %177
  %179 = load double, double* %178, align 8
  %180 = sext i32 %174 to i64
  %181 = getelementptr inbounds double, double* %tx, i64 %180
  %182 = load double, double* %181, align 8
  %183 = fmul double %182, 5.000000e-01
  %184 = fadd double %179, %183
  store double %184, double* %178, align 8
  %185 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 3
  %186 = load i32, i32* %185, align 4
  %187 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 0, i64 3
  %188 = load i32, i32* %187, align 4
  %189 = sext i32 %188 to i64
  %190 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %189
  %191 = load double, double* %190, align 8
  %192 = sext i32 %186 to i64
  %193 = getelementptr inbounds double, double* %tx, i64 %192
  %194 = load double, double* %193, align 8
  %195 = fmul double %194, 5.000000e-01
  %196 = fadd double %191, %195
  store double %196, double* %190, align 8
  br label %.loopexit7

.loopexit7:                                       ; preds = %.loopexit7.loopexit, %10
  %197 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 0, i64 1, i64 4
  %198 = load i32, i32* %197, align 4
  %199 = icmp eq i32 %198, -1
  br i1 %199, label %.loopexit5.loopexit, label %.loopexit5

.loopexit5.loopexit:                              ; preds = %.loopexit7
  %200 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 4
  %201 = load i32, i32* %200, align 4
  %202 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 1, i64 4
  %203 = load i32, i32* %202, align 4
  %204 = sext i32 %203 to i64
  %205 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %204
  %206 = load double, double* %205, align 8
  %207 = sext i32 %201 to i64
  %208 = getelementptr inbounds double, double* %tx, i64 %207
  %209 = load double, double* %208, align 8
  %210 = fmul double %209, 5.000000e-01
  %211 = fadd double %206, %210
  store double %211, double* %205, align 8
  %212 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 2, i64 4
  %213 = load i32, i32* %212, align 4
  %214 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 2, i64 4
  %215 = load i32, i32* %214, align 8
  %216 = sext i32 %215 to i64
  %217 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %216
  %218 = load double, double* %217, align 8
  %219 = sext i32 %213 to i64
  %220 = getelementptr inbounds double, double* %tx, i64 %219
  %221 = load double, double* %220, align 8
  %222 = fmul double %221, 5.000000e-01
  %223 = fadd double %218, %222
  store double %223, double* %217, align 8
  %224 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 3, i64 4
  %225 = load i32, i32* %224, align 4
  %226 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 3, i64 4
  %227 = load i32, i32* %226, align 4
  %228 = sext i32 %227 to i64
  %229 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %228
  %230 = load double, double* %229, align 8
  %231 = sext i32 %225 to i64
  %232 = getelementptr inbounds double, double* %tx, i64 %231
  %233 = load double, double* %232, align 8
  %234 = fmul double %233, 5.000000e-01
  %235 = fadd double %230, %234
  store double %235, double* %229, align 8
  br label %.loopexit5

.loopexit5:                                       ; preds = %.loopexit5.loopexit, %.loopexit7
  %236 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 1, i64 4, i64 1
  %237 = load i32, i32* %236, align 4
  %238 = icmp eq i32 %237, -1
  br i1 %238, label %.loopexit3.loopexit, label %.loopexit3

.loopexit3.loopexit:                              ; preds = %.loopexit5
  %239 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 4, i64 1
  %240 = load i32, i32* %239, align 4
  %241 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 4, i64 1
  %242 = load i32, i32* %241, align 4
  %243 = sext i32 %242 to i64
  %244 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %243
  %245 = load double, double* %244, align 8
  %246 = sext i32 %240 to i64
  %247 = getelementptr inbounds double, double* %tx, i64 %246
  %248 = load double, double* %247, align 8
  %249 = fmul double %248, 5.000000e-01
  %250 = fadd double %245, %249
  store double %250, double* %244, align 8
  %251 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 4, i64 2
  %252 = load i32, i32* %251, align 4
  %253 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 4, i64 2
  %254 = load i32, i32* %253, align 8
  %255 = sext i32 %254 to i64
  %256 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %255
  %257 = load double, double* %256, align 8
  %258 = sext i32 %252 to i64
  %259 = getelementptr inbounds double, double* %tx, i64 %258
  %260 = load double, double* %259, align 8
  %261 = fmul double %260, 5.000000e-01
  %262 = fadd double %257, %261
  store double %262, double* %256, align 8
  %263 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 4, i64 3
  %264 = load i32, i32* %263, align 4
  %265 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 4, i64 3
  %266 = load i32, i32* %265, align 4
  %267 = sext i32 %266 to i64
  %268 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %267
  %269 = load double, double* %268, align 8
  %270 = sext i32 %264 to i64
  %271 = getelementptr inbounds double, double* %tx, i64 %270
  %272 = load double, double* %271, align 8
  %273 = fmul double %272, 5.000000e-01
  %274 = fadd double %269, %273
  store double %274, double* %268, align 8
  br label %.loopexit3

.loopexit3:                                       ; preds = %.loopexit3.loopexit, %.loopexit5
  %275 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 4, i64 0
  %276 = load i32, i32* %275, align 16
  %277 = icmp eq i32 %276, -1
  br i1 %277, label %.loopexit.loopexit, label %.loopexit

.loopexit.loopexit:                               ; preds = %.loopexit3
  %278 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 0
  %279 = load i32, i32* %278, align 4
  %280 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 1, i64 0
  %281 = load i32, i32* %280, align 4
  %282 = sext i32 %281 to i64
  %283 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %282
  %284 = load double, double* %283, align 8
  %285 = sext i32 %279 to i64
  %286 = getelementptr inbounds double, double* %tx, i64 %285
  %287 = load double, double* %286, align 8
  %288 = fmul double %287, 5.000000e-01
  %289 = fadd double %284, %288
  store double %289, double* %283, align 8
  %290 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 2, i64 0
  %291 = load i32, i32* %290, align 4
  %292 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 2, i64 0
  %293 = load i32, i32* %292, align 8
  %294 = sext i32 %293 to i64
  %295 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %294
  %296 = load double, double* %295, align 8
  %297 = sext i32 %291 to i64
  %298 = getelementptr inbounds double, double* %tx, i64 %297
  %299 = load double, double* %298, align 8
  %300 = fmul double %299, 5.000000e-01
  %301 = fadd double %296, %300
  store double %301, double* %295, align 8
  %302 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 3, i64 0
  %303 = load i32, i32* %302, align 4
  %304 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 3, i64 0
  %305 = load i32, i32* %304, align 4
  %306 = sext i32 %305 to i64
  %307 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %306
  %308 = load double, double* %307, align 8
  %309 = sext i32 %303 to i64
  %310 = getelementptr inbounds double, double* %tx, i64 %309
  %311 = load double, double* %310, align 8
  %312 = fmul double %311, 5.000000e-01
  %313 = fadd double %308, %312
  store double %313, double* %307, align 8
  br label %.loopexit

.loopexit:                                        ; preds = %.loopexit.loopexit, %.loopexit3, %6
  %indvars.iv.next44 = add nuw nsw i64 %indvars.iv43, 1
  br label %.preheader8

314:                                              ; preds = %.preheader8
  %indvars.iv.next47 = add nuw nsw i64 %indvars.iv46, 1
  br label %4

315:                                              ; preds = %4
  ret void
}

; Function Attrs: nounwind uwtable
define void @transfb_c_2(double* nocapture readonly %tx) local_unnamed_addr #0 {
  %1 = load i32, i32* @nmor, align 4
  tail call void @r_init(double* getelementptr inbounds ([334600 x double], [334600 x double]* @tmort, i64 0, i64 0), i32 %1, double 0.000000e+00) #4
  %2 = load i32, i32* @nmor, align 4
  tail call void @r_init(double* getelementptr inbounds ([334600 x double], [334600 x double]* @mormult, i64 0, i64 0), i32 %2, double 0.000000e+00) #4
  %3 = load i32, i32* @nelt, align 4
  %4 = sext i32 %3 to i64
  br label %5

5:                                                ; preds = %390, %0
  %indvars.iv46 = phi i64 [ %indvars.iv.next47, %390 ], [ 0, %0 ]
  %6 = icmp slt i64 %indvars.iv46, %4
  br i1 %6, label %.preheader8, label %391

.preheader8:                                      ; preds = %.loopexit, %5
  %indvars.iv43 = phi i64 [ %indvars.iv.next44, %.loopexit ], [ 0, %5 ]
  %exitcond45 = icmp eq i64 %indvars.iv43, 6
  br i1 %exitcond45, label %390, label %7

7:                                                ; preds = %.preheader8
  %8 = getelementptr inbounds [8800 x [6 x i32]], [8800 x [6 x i32]]* @cbc, i64 0, i64 %indvars.iv46, i64 %indvars.iv43
  %9 = load i32, i32* %8, align 4
  %10 = icmp eq i32 %9, 3
  br i1 %10, label %.loopexit, label %11

11:                                               ; preds = %7
  %12 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0
  %13 = load i32, i32* %12, align 4
  %14 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 4
  %15 = load i32, i32* %14, align 4
  %16 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 4, i64 0
  %17 = load i32, i32* %16, align 4
  %18 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 4, i64 4
  %19 = load i32, i32* %18, align 4
  %20 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 0, i64 0
  %21 = load i32, i32* %20, align 16
  %22 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 0, i64 0, i64 4
  %23 = load i32, i32* %22, align 8
  %24 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 1, i64 4, i64 0
  %25 = load i32, i32* %24, align 4
  %26 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 1, i64 4, i64 4
  %27 = load i32, i32* %26, align 4
  %28 = sext i32 %21 to i64
  %29 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %28
  %30 = load double, double* %29, align 8
  %31 = sext i32 %13 to i64
  %32 = getelementptr inbounds double, double* %tx, i64 %31
  %33 = load double, double* %32, align 8
  %34 = fmul double %33, 0x3FD5555555555555
  %35 = fadd double %30, %34
  store double %35, double* %29, align 8
  %36 = sext i32 %23 to i64
  %37 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %36
  %38 = load double, double* %37, align 8
  %39 = sext i32 %15 to i64
  %40 = getelementptr inbounds double, double* %tx, i64 %39
  %41 = load double, double* %40, align 8
  %42 = fmul double %41, 0x3FD5555555555555
  %43 = fadd double %38, %42
  store double %43, double* %37, align 8
  %44 = sext i32 %25 to i64
  %45 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %44
  %46 = load double, double* %45, align 8
  %47 = sext i32 %17 to i64
  %48 = getelementptr inbounds double, double* %tx, i64 %47
  %49 = load double, double* %48, align 8
  %50 = fmul double %49, 0x3FD5555555555555
  %51 = fadd double %46, %50
  store double %51, double* %45, align 8
  %52 = sext i32 %27 to i64
  %53 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %52
  %54 = load double, double* %53, align 8
  %55 = sext i32 %19 to i64
  %56 = getelementptr inbounds double, double* %tx, i64 %55
  %57 = load double, double* %56, align 8
  %58 = fmul double %57, 0x3FD5555555555555
  %59 = fadd double %54, %58
  store double %59, double* %53, align 8
  %60 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %28
  %61 = load double, double* %60, align 8
  %62 = fadd double %61, 0x3FD5555555555555
  store double %62, double* %60, align 8
  %63 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %36
  %64 = load double, double* %63, align 8
  %65 = fadd double %64, 0x3FD5555555555555
  store double %65, double* %63, align 8
  %66 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %44
  %67 = load double, double* %66, align 8
  %68 = fadd double %67, 0x3FD5555555555555
  store double %68, double* %66, align 8
  %69 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %52
  %70 = load double, double* %69, align 8
  %71 = fadd double %70, 0x3FD5555555555555
  store double %71, double* %69, align 8
  %72 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 1
  %73 = load i32, i32* %72, align 4
  %74 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 1, i64 1
  %75 = load i32, i32* %74, align 4
  %76 = sext i32 %75 to i64
  %77 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %76
  %78 = load double, double* %77, align 8
  %79 = sext i32 %73 to i64
  %80 = getelementptr inbounds double, double* %tx, i64 %79
  %81 = load double, double* %80, align 8
  %82 = fadd double %78, %81
  store double %82, double* %77, align 8
  %83 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %76
  %84 = load double, double* %83, align 8
  %85 = fadd double %84, 1.000000e+00
  store double %85, double* %83, align 8
  %86 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 2
  %87 = load i32, i32* %86, align 4
  %88 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 1, i64 2
  %89 = load i32, i32* %88, align 4
  %90 = sext i32 %89 to i64
  %91 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %90
  %92 = load double, double* %91, align 8
  %93 = sext i32 %87 to i64
  %94 = getelementptr inbounds double, double* %tx, i64 %93
  %95 = load double, double* %94, align 8
  %96 = fadd double %92, %95
  store double %96, double* %91, align 8
  %97 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %90
  %98 = load double, double* %97, align 8
  %99 = fadd double %98, 1.000000e+00
  store double %99, double* %97, align 8
  %100 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 3
  %101 = load i32, i32* %100, align 4
  %102 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 1, i64 3
  %103 = load i32, i32* %102, align 4
  %104 = sext i32 %103 to i64
  %105 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %104
  %106 = load double, double* %105, align 8
  %107 = sext i32 %101 to i64
  %108 = getelementptr inbounds double, double* %tx, i64 %107
  %109 = load double, double* %108, align 8
  %110 = fadd double %106, %109
  store double %110, double* %105, align 8
  %111 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %104
  %112 = load double, double* %111, align 8
  %113 = fadd double %112, 1.000000e+00
  store double %113, double* %111, align 8
  %114 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 2, i64 1
  %115 = load i32, i32* %114, align 4
  %116 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 2, i64 1
  %117 = load i32, i32* %116, align 4
  %118 = sext i32 %117 to i64
  %119 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %118
  %120 = load double, double* %119, align 8
  %121 = sext i32 %115 to i64
  %122 = getelementptr inbounds double, double* %tx, i64 %121
  %123 = load double, double* %122, align 8
  %124 = fadd double %120, %123
  store double %124, double* %119, align 8
  %125 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %118
  %126 = load double, double* %125, align 8
  %127 = fadd double %126, 1.000000e+00
  store double %127, double* %125, align 8
  %128 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 2, i64 2
  %129 = load i32, i32* %128, align 4
  %130 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 2, i64 2
  %131 = load i32, i32* %130, align 8
  %132 = sext i32 %131 to i64
  %133 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %132
  %134 = load double, double* %133, align 8
  %135 = sext i32 %129 to i64
  %136 = getelementptr inbounds double, double* %tx, i64 %135
  %137 = load double, double* %136, align 8
  %138 = fadd double %134, %137
  store double %138, double* %133, align 8
  %139 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %132
  %140 = load double, double* %139, align 8
  %141 = fadd double %140, 1.000000e+00
  store double %141, double* %139, align 8
  %142 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 2, i64 3
  %143 = load i32, i32* %142, align 4
  %144 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 2, i64 3
  %145 = load i32, i32* %144, align 4
  %146 = sext i32 %145 to i64
  %147 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %146
  %148 = load double, double* %147, align 8
  %149 = sext i32 %143 to i64
  %150 = getelementptr inbounds double, double* %tx, i64 %149
  %151 = load double, double* %150, align 8
  %152 = fadd double %148, %151
  store double %152, double* %147, align 8
  %153 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %146
  %154 = load double, double* %153, align 8
  %155 = fadd double %154, 1.000000e+00
  store double %155, double* %153, align 8
  %156 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 3, i64 1
  %157 = load i32, i32* %156, align 4
  %158 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 3, i64 1
  %159 = load i32, i32* %158, align 4
  %160 = sext i32 %159 to i64
  %161 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %160
  %162 = load double, double* %161, align 8
  %163 = sext i32 %157 to i64
  %164 = getelementptr inbounds double, double* %tx, i64 %163
  %165 = load double, double* %164, align 8
  %166 = fadd double %162, %165
  store double %166, double* %161, align 8
  %167 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %160
  %168 = load double, double* %167, align 8
  %169 = fadd double %168, 1.000000e+00
  store double %169, double* %167, align 8
  %170 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 3, i64 2
  %171 = load i32, i32* %170, align 4
  %172 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 3, i64 2
  %173 = load i32, i32* %172, align 4
  %174 = sext i32 %173 to i64
  %175 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %174
  %176 = load double, double* %175, align 8
  %177 = sext i32 %171 to i64
  %178 = getelementptr inbounds double, double* %tx, i64 %177
  %179 = load double, double* %178, align 8
  %180 = fadd double %176, %179
  store double %180, double* %175, align 8
  %181 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %174
  %182 = load double, double* %181, align 8
  %183 = fadd double %182, 1.000000e+00
  store double %183, double* %181, align 8
  %184 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 3, i64 3
  %185 = load i32, i32* %184, align 4
  %186 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 3, i64 3
  %187 = load i32, i32* %186, align 4
  %188 = sext i32 %187 to i64
  %189 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %188
  %190 = load double, double* %189, align 8
  %191 = sext i32 %185 to i64
  %192 = getelementptr inbounds double, double* %tx, i64 %191
  %193 = load double, double* %192, align 8
  %194 = fadd double %190, %193
  store double %194, double* %189, align 8
  %195 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %188
  %196 = load double, double* %195, align 8
  %197 = fadd double %196, 1.000000e+00
  store double %197, double* %195, align 8
  %198 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 0, i64 4
  %199 = load i32, i32* %198, align 16
  %200 = icmp eq i32 %199, -1
  br i1 %200, label %.loopexit7.loopexit, label %.loopexit7

.loopexit7.loopexit:                              ; preds = %11
  %201 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 1
  %202 = load i32, i32* %201, align 4
  %203 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 0, i64 1
  %204 = load i32, i32* %203, align 4
  %205 = sext i32 %204 to i64
  %206 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %205
  %207 = load double, double* %206, align 8
  %208 = sext i32 %202 to i64
  %209 = getelementptr inbounds double, double* %tx, i64 %208
  %210 = load double, double* %209, align 8
  %211 = fmul double %210, 5.000000e-01
  %212 = fadd double %207, %211
  store double %212, double* %206, align 8
  %213 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %205
  %214 = load double, double* %213, align 8
  %215 = fadd double %214, 5.000000e-01
  store double %215, double* %213, align 8
  %216 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 2
  %217 = load i32, i32* %216, align 4
  %218 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 0, i64 2
  %219 = load i32, i32* %218, align 8
  %220 = sext i32 %219 to i64
  %221 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %220
  %222 = load double, double* %221, align 8
  %223 = sext i32 %217 to i64
  %224 = getelementptr inbounds double, double* %tx, i64 %223
  %225 = load double, double* %224, align 8
  %226 = fmul double %225, 5.000000e-01
  %227 = fadd double %222, %226
  store double %227, double* %221, align 8
  %228 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %220
  %229 = load double, double* %228, align 8
  %230 = fadd double %229, 5.000000e-01
  store double %230, double* %228, align 8
  %231 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 3
  %232 = load i32, i32* %231, align 4
  %233 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 0, i64 3
  %234 = load i32, i32* %233, align 4
  %235 = sext i32 %234 to i64
  %236 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %235
  %237 = load double, double* %236, align 8
  %238 = sext i32 %232 to i64
  %239 = getelementptr inbounds double, double* %tx, i64 %238
  %240 = load double, double* %239, align 8
  %241 = fmul double %240, 5.000000e-01
  %242 = fadd double %237, %241
  store double %242, double* %236, align 8
  %243 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %235
  %244 = load double, double* %243, align 8
  %245 = fadd double %244, 5.000000e-01
  store double %245, double* %243, align 8
  br label %.loopexit7

.loopexit7:                                       ; preds = %.loopexit7.loopexit, %11
  %246 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 0, i64 1, i64 4
  %247 = load i32, i32* %246, align 4
  %248 = icmp eq i32 %247, -1
  br i1 %248, label %.loopexit5.loopexit, label %.loopexit5

.loopexit5.loopexit:                              ; preds = %.loopexit7
  %249 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 4
  %250 = load i32, i32* %249, align 4
  %251 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 1, i64 4
  %252 = load i32, i32* %251, align 4
  %253 = sext i32 %252 to i64
  %254 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %253
  %255 = load double, double* %254, align 8
  %256 = sext i32 %250 to i64
  %257 = getelementptr inbounds double, double* %tx, i64 %256
  %258 = load double, double* %257, align 8
  %259 = fmul double %258, 5.000000e-01
  %260 = fadd double %255, %259
  store double %260, double* %254, align 8
  %261 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %253
  %262 = load double, double* %261, align 8
  %263 = fadd double %262, 5.000000e-01
  store double %263, double* %261, align 8
  %264 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 2, i64 4
  %265 = load i32, i32* %264, align 4
  %266 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 2, i64 4
  %267 = load i32, i32* %266, align 8
  %268 = sext i32 %267 to i64
  %269 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %268
  %270 = load double, double* %269, align 8
  %271 = sext i32 %265 to i64
  %272 = getelementptr inbounds double, double* %tx, i64 %271
  %273 = load double, double* %272, align 8
  %274 = fmul double %273, 5.000000e-01
  %275 = fadd double %270, %274
  store double %275, double* %269, align 8
  %276 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %268
  %277 = load double, double* %276, align 8
  %278 = fadd double %277, 5.000000e-01
  store double %278, double* %276, align 8
  %279 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 3, i64 4
  %280 = load i32, i32* %279, align 4
  %281 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 3, i64 4
  %282 = load i32, i32* %281, align 4
  %283 = sext i32 %282 to i64
  %284 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %283
  %285 = load double, double* %284, align 8
  %286 = sext i32 %280 to i64
  %287 = getelementptr inbounds double, double* %tx, i64 %286
  %288 = load double, double* %287, align 8
  %289 = fmul double %288, 5.000000e-01
  %290 = fadd double %285, %289
  store double %290, double* %284, align 8
  %291 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %283
  %292 = load double, double* %291, align 8
  %293 = fadd double %292, 5.000000e-01
  store double %293, double* %291, align 8
  br label %.loopexit5

.loopexit5:                                       ; preds = %.loopexit5.loopexit, %.loopexit7
  %294 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 1, i64 4, i64 1
  %295 = load i32, i32* %294, align 4
  %296 = icmp eq i32 %295, -1
  br i1 %296, label %.loopexit3.loopexit, label %.loopexit3

.loopexit3.loopexit:                              ; preds = %.loopexit5
  %297 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 4, i64 1
  %298 = load i32, i32* %297, align 4
  %299 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 4, i64 1
  %300 = load i32, i32* %299, align 4
  %301 = sext i32 %300 to i64
  %302 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %301
  %303 = load double, double* %302, align 8
  %304 = sext i32 %298 to i64
  %305 = getelementptr inbounds double, double* %tx, i64 %304
  %306 = load double, double* %305, align 8
  %307 = fmul double %306, 5.000000e-01
  %308 = fadd double %303, %307
  store double %308, double* %302, align 8
  %309 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %301
  %310 = load double, double* %309, align 8
  %311 = fadd double %310, 5.000000e-01
  store double %311, double* %309, align 8
  %312 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 4, i64 2
  %313 = load i32, i32* %312, align 4
  %314 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 4, i64 2
  %315 = load i32, i32* %314, align 8
  %316 = sext i32 %315 to i64
  %317 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %316
  %318 = load double, double* %317, align 8
  %319 = sext i32 %313 to i64
  %320 = getelementptr inbounds double, double* %tx, i64 %319
  %321 = load double, double* %320, align 8
  %322 = fmul double %321, 5.000000e-01
  %323 = fadd double %318, %322
  store double %323, double* %317, align 8
  %324 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %316
  %325 = load double, double* %324, align 8
  %326 = fadd double %325, 5.000000e-01
  store double %326, double* %324, align 8
  %327 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 4, i64 3
  %328 = load i32, i32* %327, align 4
  %329 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 4, i64 3
  %330 = load i32, i32* %329, align 4
  %331 = sext i32 %330 to i64
  %332 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %331
  %333 = load double, double* %332, align 8
  %334 = sext i32 %328 to i64
  %335 = getelementptr inbounds double, double* %tx, i64 %334
  %336 = load double, double* %335, align 8
  %337 = fmul double %336, 5.000000e-01
  %338 = fadd double %333, %337
  store double %338, double* %332, align 8
  %339 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %331
  %340 = load double, double* %339, align 8
  %341 = fadd double %340, 5.000000e-01
  store double %341, double* %339, align 8
  br label %.loopexit3

.loopexit3:                                       ; preds = %.loopexit3.loopexit, %.loopexit5
  %342 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 4, i64 0
  %343 = load i32, i32* %342, align 16
  %344 = icmp eq i32 %343, -1
  br i1 %344, label %.loopexit.loopexit, label %.loopexit

.loopexit.loopexit:                               ; preds = %.loopexit3
  %345 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 1, i64 0
  %346 = load i32, i32* %345, align 4
  %347 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 1, i64 0
  %348 = load i32, i32* %347, align 4
  %349 = sext i32 %348 to i64
  %350 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %349
  %351 = load double, double* %350, align 8
  %352 = sext i32 %346 to i64
  %353 = getelementptr inbounds double, double* %tx, i64 %352
  %354 = load double, double* %353, align 8
  %355 = fmul double %354, 5.000000e-01
  %356 = fadd double %351, %355
  store double %356, double* %350, align 8
  %357 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %349
  %358 = load double, double* %357, align 8
  %359 = fadd double %358, 5.000000e-01
  store double %359, double* %357, align 8
  %360 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 2, i64 0
  %361 = load i32, i32* %360, align 4
  %362 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 2, i64 0
  %363 = load i32, i32* %362, align 8
  %364 = sext i32 %363 to i64
  %365 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %364
  %366 = load double, double* %365, align 8
  %367 = sext i32 %361 to i64
  %368 = getelementptr inbounds double, double* %tx, i64 %367
  %369 = load double, double* %368, align 8
  %370 = fmul double %369, 5.000000e-01
  %371 = fadd double %366, %370
  store double %371, double* %365, align 8
  %372 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %364
  %373 = load double, double* %372, align 8
  %374 = fadd double %373, 5.000000e-01
  store double %374, double* %372, align 8
  %375 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 3, i64 0
  %376 = load i32, i32* %375, align 4
  %377 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv46, i64 %indvars.iv43, i64 0, i64 0, i64 3, i64 0
  %378 = load i32, i32* %377, align 4
  %379 = sext i32 %378 to i64
  %380 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %379
  %381 = load double, double* %380, align 8
  %382 = sext i32 %376 to i64
  %383 = getelementptr inbounds double, double* %tx, i64 %382
  %384 = load double, double* %383, align 8
  %385 = fmul double %384, 5.000000e-01
  %386 = fadd double %381, %385
  store double %386, double* %380, align 8
  %387 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %379
  %388 = load double, double* %387, align 8
  %389 = fadd double %388, 5.000000e-01
  store double %389, double* %387, align 8
  br label %.loopexit

.loopexit:                                        ; preds = %.loopexit.loopexit, %.loopexit3, %7
  %indvars.iv.next44 = add nuw nsw i64 %indvars.iv43, 1
  br label %.preheader8

390:                                              ; preds = %.preheader8
  %indvars.iv.next47 = add nuw nsw i64 %indvars.iv46, 1
  br label %5

391:                                              ; preds = %5
  ret void
}

; Function Attrs: nounwind willreturn
declare void @llvm.assume(i1) #3

attributes #0 = { nounwind uwtable "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nofree norecurse nounwind uwtable "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind willreturn }
attributes #4 = { nounwind }
