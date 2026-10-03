source_filename = "-"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@qbnew = external local_unnamed_addr global [2 x [5 x [3 x double]]], align 16

declare void @r_init(double*, i32, double) local_unnamed_addr #0

; Function Attrs: nounwind uwtable
define void @transfb_nc0([5 x double]* %tmor, [5 x [5 x double]]* nocapture readonly %tx) local_unnamed_addr #1 {
  %1 = getelementptr [5 x double], [5 x double]* %tmor, i64 0, i64 0
  tail call void @r_init(double* %1, i32 25, double 0.000000e+00) #2
  br label %2

2:                                                ; preds = %14, %0
  %indvars.iv1 = phi i64 [ %indvars.iv.next2, %14 ], [ 0, %0 ]
  %exitcond3 = icmp eq i64 %indvars.iv1, 5
  br i1 %exitcond3, label %15, label %.preheader

.preheader:                                       ; preds = %2
  %3 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 %indvars.iv1
  br label %4

4:                                                ; preds = %5, %.preheader
  %indvars.iv = phi i64 [ 1, %.preheader ], [ %indvars.iv.next, %5 ]
  %exitcond = icmp eq i64 %indvars.iv, 4
  br i1 %exitcond, label %14, label %5

5:                                                ; preds = %4
  %6 = load double, double* %3, align 8
  %7 = add nsw i64 %indvars.iv, -1
  %8 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv1, i64 %7
  %9 = load double, double* %8, align 8
  %10 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 %indvars.iv
  %11 = load double, double* %10, align 8
  %12 = fmul double %9, %11
  %13 = fadd double %6, %12
  store double %13, double* %3, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  br label %4, !llvm.loop !0

14:                                               ; preds = %4
  %indvars.iv.next2 = add nuw nsw i64 %indvars.iv1, 1
  br label %2, !llvm.loop !2

15:                                               ; preds = %2
  ret void
}

attributes #0 = { "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind uwtable "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind }

!0 = distinct !{!0, !1}
!1 = !{!"llvm.loop.unroll.disable"}
!2 = distinct !{!2, !1}
