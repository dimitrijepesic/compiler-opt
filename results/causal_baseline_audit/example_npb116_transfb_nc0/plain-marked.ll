source_filename = "-"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@qbnew = external global [2 x [5 x [3 x double]]], align 16

declare void @r_init(double*, i32, double) #0

; Function Attrs: nounwind uwtable
define void @transfb_nc0([5 x double]* %tmor, [5 x [5 x double]]* %tx) #1 {
  %1 = alloca [5 x double]*, align 8
  %2 = alloca [5 x [5 x double]]*, align 8
  %i = alloca i32, align 4
  %j = alloca i32, align 4
  store [5 x double]* %tmor, [5 x double]** %1, align 8
  store [5 x [5 x double]]* %tx, [5 x [5 x double]]** %2, align 8
  %3 = load [5 x double]*, [5 x double]** %1, align 8
  %4 = bitcast [5 x double]* %3 to double*
  call void @r_init(double* %4, i32 25, double 0.000000e+00)
  store i32 0, i32* %j, align 4
  br label %5

5:                                                ; preds = %45, %0
  %6 = load i32, i32* %j, align 4
  %7 = icmp slt i32 %6, 5
  br i1 %7, label %8, label %48

8:                                                ; preds = %5
  store i32 1, i32* %i, align 4
  br label %9

9:                                                ; preds = %41, %8
  %10 = load i32, i32* %i, align 4
  %11 = icmp slt i32 %10, 4
  br i1 %11, label %12, label %44

12:                                               ; preds = %9
  %13 = load i32, i32* %j, align 4
  %14 = sext i32 %13 to i64
  %15 = load [5 x double]*, [5 x double]** %1, align 8
  %16 = getelementptr inbounds [5 x double], [5 x double]* %15, i64 0
  %17 = getelementptr inbounds [5 x double], [5 x double]* %16, i64 0, i64 %14
  %18 = load double, double* %17, align 8
  %19 = load i32, i32* %i, align 4
  %20 = sub nsw i32 %19, 1
  %21 = sext i32 %20 to i64
  %22 = load i32, i32* %j, align 4
  %23 = sext i32 %22 to i64
  %24 = getelementptr inbounds [5 x [3 x double]], [5 x [3 x double]]* getelementptr inbounds ([2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0), i64 0, i64 %23
  %25 = getelementptr inbounds [3 x double], [3 x double]* %24, i64 0, i64 %21
  %26 = load double, double* %25, align 8
  %27 = load i32, i32* %i, align 4
  %28 = sext i32 %27 to i64
  %29 = load [5 x [5 x double]]*, [5 x [5 x double]]** %2, align 8
  %30 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %29, i64 0
  %31 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %30, i64 0, i64 0
  %32 = getelementptr inbounds [5 x double], [5 x double]* %31, i64 0, i64 %28
  %33 = load double, double* %32, align 8
  %34 = fmul double %26, %33
  %35 = fadd double %18, %34
  %36 = load i32, i32* %j, align 4
  %37 = sext i32 %36 to i64
  %38 = load [5 x double]*, [5 x double]** %1, align 8
  %39 = getelementptr inbounds [5 x double], [5 x double]* %38, i64 0
  %40 = getelementptr inbounds [5 x double], [5 x double]* %39, i64 0, i64 %37
  store double %35, double* %40, align 8
  br label %41

41:                                               ; preds = %12
  %42 = load i32, i32* %i, align 4
  %43 = add nsw i32 %42, 1
  store i32 %43, i32* %i, align 4
  br label %9, !llvm.loop !0

44:                                               ; preds = %9
  br label %45

45:                                               ; preds = %44
  %46 = load i32, i32* %j, align 4
  %47 = add nsw i32 %46, 1
  store i32 %47, i32* %j, align 4
  br label %5, !llvm.loop !2

48:                                               ; preds = %5
  ret void
}

attributes #0 = { "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind uwtable "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }

!0 = distinct !{!0, !1}
!1 = !{!"llvm.loop.unroll.disable"}
!2 = distinct !{!2, !1}
