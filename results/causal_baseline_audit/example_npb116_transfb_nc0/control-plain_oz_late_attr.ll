source_filename = "-"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@qbnew = external local_unnamed_addr global [2 x [5 x [3 x double]]], align 16

declare void @r_init(double*, i32, double) local_unnamed_addr #0

; Function Attrs: minsize nounwind optsize uwtable
define void @transfb_nc0([5 x double]* %tmor, [5 x [5 x double]]* nocapture readonly %tx) local_unnamed_addr #1 {
  %1 = getelementptr [5 x double], [5 x double]* %tmor, i64 0, i64 0
  tail call void @r_init(double* %1, i32 25, double 0.000000e+00) #2
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

attributes #0 = { "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { minsize nounwind optsize uwtable "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind }
