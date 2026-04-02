; ModuleID = '-'
source_filename = "-"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%struct._IO_FILE = type { i32, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, %struct._IO_marker*, %struct._IO_FILE*, i32, i32, i64, i16, i8, [1 x i8], i8*, i64, %struct._IO_codecvt*, %struct._IO_wide_data*, %struct._IO_FILE*, i8*, i64, i32, [20 x i8] }
%struct._IO_marker = type opaque
%struct._IO_codecvt = type opaque
%struct._IO_wide_data = type opaque
%struct.my3DVertexStruct = type { i32, i32, i32, double }

@stderr = external dso_local global %struct._IO_FILE*, align 8
@.str = private unnamed_addr constant [27 x i8] c"Usage: qsort_large <file>\0A\00", align 1
@.str.1 = private unnamed_addr constant [2 x i8] c"r\00", align 1
@.str.2 = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.3 = private unnamed_addr constant [57 x i8] c"\0ASorting %d vectors based on distance from the origin.\0A\0A\00", align 1
@.str.4 = private unnamed_addr constant [18 x i8] c"sorted_output.dat\00", align 1
@.str.5 = private unnamed_addr constant [3 x i8] c"wt\00", align 1
@.str.6 = private unnamed_addr constant [32 x i8] c"\0AError: Can't open output file\0A\00", align 1
@.str.7 = private unnamed_addr constant [10 x i8] c"%d %d %d\0A\00", align 1
@.str.8 = private unnamed_addr constant [15 x i8] c"_finfo_dataset\00", align 1
@.str.1.9 = private unnamed_addr constant [3 x i8] c"rt\00", align 1
@.str.2.10 = private unnamed_addr constant [29 x i8] c"\0AError: Can't find dataset!\0A\00", align 1
@.str.3.11 = private unnamed_addr constant [4 x i8] c"%ld\00", align 1

; Function Attrs: nounwind uwtable
define dso_local i32 @compare(i8* %0, i8* %1) #0 {
  %3 = getelementptr inbounds i8, i8* %0, i64 16
  %4 = bitcast i8* %3 to double*
  %5 = load double, double* %4, align 8, !tbaa !0
  %6 = getelementptr inbounds i8, i8* %1, i64 16
  %7 = bitcast i8* %6 to double*
  %8 = load double, double* %7, align 8, !tbaa !0
  %9 = fcmp ogt double %5, %8
  %10 = fcmp une double %5, %8
  %11 = sext i1 %10 to i32
  %12 = select i1 %9, i32 1, i32 %11
  ret i32 %12
}

; Function Attrs: argmemonly nounwind willreturn
declare void @llvm.lifetime.start.p0i8(i64 immarg, i8* nocapture) #1

; Function Attrs: argmemonly nounwind willreturn
declare void @llvm.lifetime.end.p0i8(i64 immarg, i8* nocapture) #1

; Function Attrs: nounwind uwtable
define dso_local i32 @main1(i32 %0, i8** %1, i32 %2) #0 {
  %4 = alloca [60000 x %struct.my3DVertexStruct], align 16
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = bitcast [60000 x %struct.my3DVertexStruct]* %4 to i8*
  call void @llvm.lifetime.start.p0i8(i64 1440000, i8* nonnull %8) #6
  %9 = bitcast i32* %5 to i8*
  call void @llvm.lifetime.start.p0i8(i64 4, i8* nonnull %9) #6
  %10 = bitcast i32* %6 to i8*
  call void @llvm.lifetime.start.p0i8(i64 4, i8* nonnull %10) #6
  %11 = bitcast i32* %7 to i8*
  call void @llvm.lifetime.start.p0i8(i64 4, i8* nonnull %11) #6
  %12 = icmp slt i32 %0, 2
  br i1 %12, label %13, label %16

13:                                               ; preds = %3
  %14 = load %struct._IO_FILE*, %struct._IO_FILE** @stderr, align 8, !tbaa !6
  %15 = call i64 @fwrite(i8* getelementptr inbounds ([27 x i8], [27 x i8]* @.str, i64 0, i64 0), i64 26, i64 1, %struct._IO_FILE* %14) #7
  call void @exit(i32 1) #8
  unreachable

16:                                               ; preds = %3
  %17 = getelementptr inbounds i8*, i8** %1, i64 1
  %18 = load i8*, i8** %17, align 8, !tbaa !6
  %19 = call %struct._IO_FILE* @fopen(i8* %18, i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.1, i64 0, i64 0)) #6
  br label %20

20:                                               ; preds = %30, %16
  %.0 = phi i32 [ 0, %16 ], [ %45, %30 ]
  %21 = call i32 (%struct._IO_FILE*, i8*, ...) @__isoc99_fscanf(%struct._IO_FILE* %19, i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.2, i64 0, i64 0), i32* nonnull %5) #6
  %22 = icmp eq i32 %21, 1
  br i1 %22, label %23, label %.critedge

23:                                               ; preds = %20
  %24 = call i32 (%struct._IO_FILE*, i8*, ...) @__isoc99_fscanf(%struct._IO_FILE* %19, i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.2, i64 0, i64 0), i32* nonnull %6) #6
  %25 = icmp eq i32 %24, 1
  br i1 %25, label %26, label %.critedge

26:                                               ; preds = %23
  %27 = call i32 (%struct._IO_FILE*, i8*, ...) @__isoc99_fscanf(%struct._IO_FILE* %19, i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.2, i64 0, i64 0), i32* nonnull %7) #6
  %28 = icmp eq i32 %27, 1
  %29 = icmp ult i32 %.0, 60000
  %spec.select = and i1 %28, %29
  br i1 %spec.select, label %30, label %.critedge

30:                                               ; preds = %26
  %31 = load i32, i32* %5, align 4, !tbaa !8
  %32 = zext i32 %.0 to i64
  %33 = getelementptr inbounds [60000 x %struct.my3DVertexStruct], [60000 x %struct.my3DVertexStruct]* %4, i64 0, i64 %32, i32 0
  store i32 %31, i32* %33, align 8, !tbaa !9
  %34 = load i32, i32* %6, align 4, !tbaa !8
  %35 = getelementptr inbounds [60000 x %struct.my3DVertexStruct], [60000 x %struct.my3DVertexStruct]* %4, i64 0, i64 %32, i32 1
  store i32 %34, i32* %35, align 4, !tbaa !10
  %36 = load i32, i32* %7, align 4, !tbaa !8
  %37 = getelementptr inbounds [60000 x %struct.my3DVertexStruct], [60000 x %struct.my3DVertexStruct]* %4, i64 0, i64 %32, i32 2
  store i32 %36, i32* %37, align 8, !tbaa !11
  %38 = sitofp i32 %31 to double
  %square = fmul double %38, %38
  %39 = sitofp i32 %34 to double
  %square4 = fmul double %39, %39
  %40 = fadd double %square, %square4
  %41 = sitofp i32 %36 to double
  %square5 = fmul double %41, %41
  %42 = fadd double %40, %square5
  %43 = call double @sqrt(double %42) #6
  %44 = getelementptr inbounds [60000 x %struct.my3DVertexStruct], [60000 x %struct.my3DVertexStruct]* %4, i64 0, i64 %32, i32 3
  store double %43, double* %44, align 8, !tbaa !0
  %45 = add nuw nsw i32 %.0, 1
  br label %20

.critedge:                                        ; preds = %20, %23, %26
  %46 = call i32 @fclose(%struct._IO_FILE* %19) #6
  %47 = icmp eq i32 %2, 0
  br i1 %47, label %.critedge3, label %48

48:                                               ; preds = %.critedge
  %49 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([57 x i8], [57 x i8]* @.str.3, i64 0, i64 0), i32 %.0) #6
  call void @qsortx(i8* nonnull %8, i32 %.0, i32 24, i32 (i8*, i8*)* nonnull @compare)
  %50 = call %struct._IO_FILE* @fopen(i8* getelementptr inbounds ([18 x i8], [18 x i8]* @.str.4, i64 0, i64 0), i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.5, i64 0, i64 0)) #6
  %51 = icmp eq %struct._IO_FILE* %50, null
  br i1 %51, label %52, label %55

52:                                               ; preds = %48
  %53 = load %struct._IO_FILE*, %struct._IO_FILE** @stderr, align 8, !tbaa !6
  %54 = call i64 @fwrite(i8* getelementptr inbounds ([32 x i8], [32 x i8]* @.str.6, i64 0, i64 0), i64 31, i64 1, %struct._IO_FILE* %53) #7
  call void @exit(i32 1) #8
  unreachable

55:                                               ; preds = %48, %57
  %.01 = phi i32 [ %67, %57 ], [ 0, %48 ]
  %56 = icmp ult i32 %.01, %.0
  br i1 %56, label %57, label %68

57:                                               ; preds = %55
  %58 = zext i32 %.01 to i64
  %59 = getelementptr inbounds [60000 x %struct.my3DVertexStruct], [60000 x %struct.my3DVertexStruct]* %4, i64 0, i64 %58, i32 0
  %60 = load i32, i32* %59, align 8, !tbaa !9
  %61 = getelementptr inbounds [60000 x %struct.my3DVertexStruct], [60000 x %struct.my3DVertexStruct]* %4, i64 0, i64 %58, i32 1
  %62 = load i32, i32* %61, align 4, !tbaa !10
  %63 = getelementptr inbounds [60000 x %struct.my3DVertexStruct], [60000 x %struct.my3DVertexStruct]* %4, i64 0, i64 %58, i32 2
  %64 = load i32, i32* %63, align 8, !tbaa !11
  %65 = call i32 (%struct._IO_FILE*, i8*, ...) @fprintf(%struct._IO_FILE* nonnull %50, i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.7, i64 0, i64 0), i32 %60, i32 %62, i32 %64) #6
  %66 = udiv i32 %.0, 100
  %67 = add nuw nsw i32 %.01, %66
  br label %55

68:                                               ; preds = %55
  %69 = call i32 @fclose(%struct._IO_FILE* nonnull %50) #6
  br label %70

.critedge3:                                       ; preds = %.critedge
  call void @qsortx(i8* nonnull %8, i32 %.0, i32 24, i32 (i8*, i8*)* nonnull @compare)
  br label %70

70:                                               ; preds = %.critedge3, %68
  call void @llvm.lifetime.end.p0i8(i64 4, i8* nonnull %11) #6
  call void @llvm.lifetime.end.p0i8(i64 4, i8* nonnull %10) #6
  call void @llvm.lifetime.end.p0i8(i64 4, i8* nonnull %9) #6
  call void @llvm.lifetime.end.p0i8(i64 1440000, i8* nonnull %8) #6
  ret i32 0
}

declare dso_local i32 @fprintf(%struct._IO_FILE*, i8*, ...) #2

; Function Attrs: noreturn nounwind
declare dso_local void @exit(i32) #3

declare dso_local %struct._IO_FILE* @fopen(i8*, i8*) #2

declare dso_local i32 @__isoc99_fscanf(%struct._IO_FILE*, i8*, ...) #2

; Function Attrs: nounwind
declare dso_local double @pow(double, double) #4

; Function Attrs: nounwind
declare dso_local double @sqrt(double) #4

declare dso_local i32 @fclose(%struct._IO_FILE*) #2

declare dso_local i32 @printf(i8*, ...) #2

; Function Attrs: nounwind uwtable
define dso_local i32 @main(i32 %0, i8** %1) #0 {
  %3 = alloca i64, align 8
  %4 = bitcast i64* %3 to i8*
  call void @llvm.lifetime.start.p0i8(i64 8, i8* nonnull %4) #6
  %5 = call %struct._IO_FILE* @fopen(i8* getelementptr inbounds ([15 x i8], [15 x i8]* @.str.8, i64 0, i64 0), i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.1.9, i64 0, i64 0)) #6
  %6 = icmp eq %struct._IO_FILE* %5, null
  br i1 %6, label %7, label %10

7:                                                ; preds = %2
  %8 = load %struct._IO_FILE*, %struct._IO_FILE** @stderr, align 8, !tbaa !6
  %9 = call i64 @fwrite(i8* getelementptr inbounds ([29 x i8], [29 x i8]* @.str.2.10, i64 0, i64 0), i64 28, i64 1, %struct._IO_FILE* %8) #7
  br label %21

10:                                               ; preds = %2
  %11 = call i32 (%struct._IO_FILE*, i8*, ...) @__isoc99_fscanf(%struct._IO_FILE* nonnull %5, i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.3.11, i64 0, i64 0), i64* nonnull %3) #6
  %12 = call i32 @fclose(%struct._IO_FILE* nonnull %5) #6
  br label %13

13:                                               ; preds = %16, %10
  %.01 = phi i64 [ 0, %10 ], [ %17, %16 ]
  %14 = load i64, i64* %3, align 8, !tbaa !12
  %15 = icmp slt i64 %.01, %14
  br i1 %15, label %16, label %21

16:                                               ; preds = %13
  %17 = add nuw nsw i64 %.01, 1
  %18 = icmp eq i64 %17, %14
  %19 = zext i1 %18 to i32
  %20 = call i32 @main1(i32 %0, i8** %1, i32 %19)
  br label %13

21:                                               ; preds = %13, %7
  %.0 = phi i32 [ 1, %7 ], [ 0, %13 ]
  call void @llvm.lifetime.end.p0i8(i64 8, i8* nonnull %4) #6
  ret i32 %.0
}

; Function Attrs: nounwind uwtable
define dso_local void @qsortx(i8* %0, i32 %1, i32 %2, i32 (i8*, i8*)* %3) #0 {
  %5 = alloca [30 x i8*], align 16
  %6 = alloca [30 x i8*], align 16
  %7 = bitcast [30 x i8*]* %5 to i8*
  call void @llvm.lifetime.start.p0i8(i64 240, i8* nonnull %7) #6
  %8 = bitcast [30 x i8*]* %6 to i8*
  call void @llvm.lifetime.start.p0i8(i64 240, i8* nonnull %8) #6
  %9 = icmp ult i32 %1, 2
  %10 = icmp eq i32 %2, 0
  %or.cond = or i1 %9, %10
  br i1 %or.cond, label %86, label %11

11:                                               ; preds = %4
  %12 = add i32 %1, -1
  %13 = mul i32 %12, %2
  %14 = zext i32 %13 to i64
  %15 = getelementptr inbounds i8, i8* %0, i64 %14
  br label %16

16:                                               ; preds = %65, %80, %75, %11
  %.06 = phi i8* [ %15, %11 ], [ %85, %80 ], [ %76, %75 ], [ %.06, %65 ]
  %.05 = phi i8* [ %0, %11 ], [ %83, %80 ], [ %.05, %75 ], [ %34, %65 ]
  %.0 = phi i32 [ 0, %11 ], [ %78, %80 ], [ %.2, %75 ], [ %.1, %65 ]
  %17 = ptrtoint i8* %.06 to i64
  %18 = ptrtoint i8* %.05 to i64
  %19 = sub i64 %17, %18
  %20 = zext i32 %2 to i64
  %21 = sdiv i64 %19, %20
  %22 = trunc i64 %21 to i32
  %23 = add i32 %22, 1
  %24 = icmp ult i32 %23, 9
  br i1 %24, label %25, label %26

25:                                               ; preds = %16
  call void @shortsort(i8* %.05, i8* %.06, i32 %2, i32 (i8*, i8*)* %3)
  br label %77

26:                                               ; preds = %16
  %27 = lshr i32 %23, 1
  %28 = mul i32 %27, %2
  %29 = zext i32 %28 to i64
  %30 = getelementptr inbounds i8, i8* %.05, i64 %29
  call void @swap(i8* %30, i8* %.05, i32 %2)
  %31 = getelementptr inbounds i8, i8* %.06, i64 %20
  br label %32

32:                                               ; preds = %55, %26
  %.03 = phi i8* [ %.05, %26 ], [ %34, %55 ]
  %.01 = phi i8* [ %31, %26 ], [ %41, %55 ]
  br label %33

33:                                               ; preds = %36, %32
  %.14 = phi i8* [ %.03, %32 ], [ %34, %36 ]
  %34 = getelementptr inbounds i8, i8* %.14, i64 %20
  %35 = icmp ugt i8* %34, %.06
  br i1 %35, label %.critedge, label %36

36:                                               ; preds = %33
  %37 = call i32 %3(i8* %34, i8* %.05) #6
  %38 = icmp slt i32 %37, 1
  br i1 %38, label %33, label %.critedge

.critedge:                                        ; preds = %33, %36
  br label %39

39:                                               ; preds = %43, %.critedge
  %.12 = phi i8* [ %.01, %.critedge ], [ %41, %43 ]
  %40 = sub nsw i64 0, %20
  %41 = getelementptr inbounds i8, i8* %.12, i64 %40
  %42 = icmp ugt i8* %41, %.05
  br i1 %42, label %43, label %.critedge7

43:                                               ; preds = %39
  %44 = call i32 %3(i8* %41, i8* %.05) #6
  %45 = icmp sgt i32 %44, -1
  br i1 %45, label %39, label %.critedge7

.critedge7:                                       ; preds = %39, %43
  %46 = icmp ult i8* %41, %34
  br i1 %46, label %47, label %55

47:                                               ; preds = %.critedge7
  call void @swap(i8* %.05, i8* %41, i32 %2)
  %48 = getelementptr inbounds i8, i8* %41, i64 -1
  %49 = ptrtoint i8* %48 to i64
  %50 = sub i64 %49, %18
  %51 = ptrtoint i8* %34 to i64
  %52 = sub i64 %17, %51
  %53 = icmp slt i64 %50, %52
  %54 = icmp ult i8* %34, %.06
  br i1 %53, label %66, label %56

55:                                               ; preds = %.critedge7
  call void @swap(i8* %34, i8* %41, i32 %2)
  br label %32

56:                                               ; preds = %47
  %57 = getelementptr inbounds i8, i8* %.05, i64 %20
  %58 = icmp ult i8* %57, %41
  br i1 %58, label %59, label %65

59:                                               ; preds = %56
  %60 = sext i32 %.0 to i64
  %61 = getelementptr inbounds [30 x i8*], [30 x i8*]* %5, i64 0, i64 %60
  store i8* %.05, i8** %61, align 8, !tbaa !6
  %62 = getelementptr inbounds i8, i8* %41, i64 %40
  %63 = getelementptr inbounds [30 x i8*], [30 x i8*]* %6, i64 0, i64 %60
  store i8* %62, i8** %63, align 8, !tbaa !6
  %64 = add nsw i32 %.0, 1
  br label %65

65:                                               ; preds = %59, %56
  %.1 = phi i32 [ %64, %59 ], [ %.0, %56 ]
  br i1 %54, label %16, label %77

66:                                               ; preds = %47
  br i1 %54, label %67, label %72

67:                                               ; preds = %66
  %68 = sext i32 %.0 to i64
  %69 = getelementptr inbounds [30 x i8*], [30 x i8*]* %5, i64 0, i64 %68
  store i8* %34, i8** %69, align 8, !tbaa !6
  %70 = getelementptr inbounds [30 x i8*], [30 x i8*]* %6, i64 0, i64 %68
  store i8* %.06, i8** %70, align 8, !tbaa !6
  %71 = add nsw i32 %.0, 1
  br label %72

72:                                               ; preds = %67, %66
  %.2 = phi i32 [ %71, %67 ], [ %.0, %66 ]
  %73 = getelementptr inbounds i8, i8* %.05, i64 %20
  %74 = icmp ult i8* %73, %41
  br i1 %74, label %75, label %77

75:                                               ; preds = %72
  %76 = getelementptr inbounds i8, i8* %41, i64 %40
  br label %16

77:                                               ; preds = %65, %72, %25
  %.4 = phi i32 [ %.0, %25 ], [ %.1, %65 ], [ %.2, %72 ]
  %78 = add nsw i32 %.4, -1
  %79 = icmp sgt i32 %.4, 0
  br i1 %79, label %80, label %86

80:                                               ; preds = %77
  %81 = sext i32 %78 to i64
  %82 = getelementptr inbounds [30 x i8*], [30 x i8*]* %5, i64 0, i64 %81
  %83 = load i8*, i8** %82, align 8, !tbaa !6
  %84 = getelementptr inbounds [30 x i8*], [30 x i8*]* %6, i64 0, i64 %81
  %85 = load i8*, i8** %84, align 8, !tbaa !6
  br label %16

86:                                               ; preds = %77, %4
  call void @llvm.lifetime.end.p0i8(i64 240, i8* nonnull %8) #6
  call void @llvm.lifetime.end.p0i8(i64 240, i8* nonnull %7) #6
  ret void
}

; Function Attrs: nounwind uwtable
define internal void @shortsort(i8* %0, i8* %1, i32 %2, i32 (i8*, i8*)* %3) #0 {
  br label %5

5:                                                ; preds = %14, %4
  %.01 = phi i8* [ %1, %4 ], [ %16, %14 ]
  %6 = icmp ugt i8* %.01, %0
  br i1 %6, label %7, label %17

7:                                                ; preds = %5
  %8 = zext i32 %2 to i64
  br label %9

9:                                                ; preds = %11, %7
  %.pn = phi i8* [ %0, %7 ], [ %.02, %11 ]
  %.0 = phi i8* [ %0, %7 ], [ %spec.select, %11 ]
  %.02 = getelementptr inbounds i8, i8* %.pn, i64 %8
  %10 = icmp ugt i8* %.02, %.01
  br i1 %10, label %14, label %11

11:                                               ; preds = %9
  %12 = call i32 %3(i8* %.02, i8* %.0) #6
  %13 = icmp sgt i32 %12, 0
  %spec.select = select i1 %13, i8* %.02, i8* %.0
  br label %9

14:                                               ; preds = %9
  call void @swap(i8* %.0, i8* %.01, i32 %2)
  %15 = sub nsw i64 0, %8
  %16 = getelementptr inbounds i8, i8* %.01, i64 %15
  br label %5

17:                                               ; preds = %5
  ret void
}

; Function Attrs: nounwind uwtable
define internal void @swap(i8* %0, i8* %1, i32 %2) #0 {
  %4 = icmp eq i8* %0, %1
  br i1 %4, label %13, label %5

5:                                                ; preds = %3, %7
  %.02 = phi i32 [ %8, %7 ], [ %2, %3 ]
  %.01 = phi i8* [ %12, %7 ], [ %1, %3 ]
  %.0 = phi i8* [ %11, %7 ], [ %0, %3 ]
  %6 = icmp eq i32 %.02, 0
  br i1 %6, label %13, label %7

7:                                                ; preds = %5
  %8 = add i32 %.02, -1
  %9 = load i8, i8* %.0, align 1, !tbaa !14
  %10 = load i8, i8* %.01, align 1, !tbaa !14
  %11 = getelementptr inbounds i8, i8* %.0, i64 1
  store i8 %10, i8* %.0, align 1, !tbaa !14
  %12 = getelementptr inbounds i8, i8* %.01, i64 1
  store i8 %9, i8* %.01, align 1, !tbaa !14
  br label %5

13:                                               ; preds = %5, %3
  ret void
}

; Function Attrs: nofree nounwind
declare i64 @fwrite(i8* nocapture, i64, i64, %struct._IO_FILE* nocapture) #5

attributes #0 = { nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="none" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { argmemonly nounwind willreturn }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="none" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { noreturn nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="none" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="none" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #5 = { nofree nounwind }
attributes #6 = { nounwind }
attributes #7 = { cold }
attributes #8 = { noreturn nounwind }

!0 = !{!1, !5, i64 16}
!1 = !{!"my3DVertexStruct", !2, i64 0, !2, i64 4, !2, i64 8, !5, i64 16}
!2 = !{!"int", !3, i64 0}
!3 = !{!"omnipotent char", !4, i64 0}
!4 = !{!"Simple C/C++ TBAA"}
!5 = !{!"double", !3, i64 0}
!6 = !{!7, !7, i64 0}
!7 = !{!"any pointer", !3, i64 0}
!8 = !{!2, !2, i64 0}
!9 = !{!1, !2, i64 0}
!10 = !{!1, !2, i64 4}
!11 = !{!1, !2, i64 8}
!12 = !{!13, !13, i64 0}
!13 = !{!"long", !3, i64 0}
!14 = !{!3, !3, i64 0}
