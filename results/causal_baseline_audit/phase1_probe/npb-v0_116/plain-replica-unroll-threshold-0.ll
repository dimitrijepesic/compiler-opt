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
  tail call void @col2(double* %tx, double* getelementptr inbounds ([8800 x [5 x [5 x [5 x double]]]], [8800 x [5 x [5 x [5 x double]]]]* @tmult, i64 0, i64 0, i64 0, i64 0, i64 0), i32 %1) #3
  %2 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 0, i64 0, i64 0
  br label %3

3:                                                ; preds = %314, %0
  %indvars.iv130 = phi i64 [ %indvars.iv.next131, %314 ], [ 0, %0 ]
  %4 = load i32, i32* @nelt, align 4
  %5 = sext i32 %4 to i64
  %6 = icmp slt i64 %indvars.iv130, %5
  br i1 %6, label %.preheader29, label %315

.preheader29:                                     ; preds = %.loopexit, %3
  %indvars.iv127 = phi i64 [ %indvars.iv.next128, %.loopexit ], [ 0, %3 ]
  %exitcond129 = icmp eq i64 %indvars.iv127, 6
  br i1 %exitcond129, label %314, label %7

7:                                                ; preds = %.preheader29
  %8 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 0
  %9 = load i32, i32* %8, align 4
  %10 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 4
  %11 = load i32, i32* %10, align 4
  %12 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 4, i64 0
  %13 = load i32, i32* %12, align 4
  %14 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 4, i64 4
  %15 = load i32, i32* %14, align 4
  %16 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 0, i64 0, i64 0
  %17 = load i32, i32* %16, align 16
  %18 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 1, i64 0, i64 0, i64 4
  %19 = load i32, i32* %18, align 8
  %20 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 1, i64 4, i64 0
  %21 = load i32, i32* %20, align 4
  %22 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 1, i64 1, i64 4, i64 4
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
  %52 = getelementptr inbounds [8800 x [6 x i32]], [8800 x [6 x i32]]* @cbc, i64 0, i64 %indvars.iv130, i64 %indvars.iv127
  %53 = load i32, i32* %52, align 4
  %54 = icmp eq i32 %53, 3
  br i1 %54, label %55, label %.preheader28

55:                                               ; preds = %7
  call void @r_init(double* nonnull %2, i32 50, double 0.000000e+00) #3
  br label %56

56:                                               ; preds = %88, %55
  %indvars.iv98 = phi i64 [ %indvars.iv.next99, %88 ], [ 0, %55 ]
  %exitcond101 = icmp eq i64 %indvars.iv98, 2
  br i1 %exitcond101, label %.preheader11, label %.preheader9

.preheader9:                                      ; preds = %87, %56
  %indvars.iv95 = phi i64 [ %indvars.iv.next96, %87 ], [ 0, %56 ]
  %exitcond97 = icmp eq i64 %indvars.iv95, 2
  br i1 %exitcond97, label %88, label %.preheader1

.preheader1:                                      ; preds = %.preheader9
  %57 = getelementptr inbounds [2 x i32], [2 x i32]* @v_end, i64 0, i64 %indvars.iv95
  %58 = load i32, i32* %57, align 4
  %59 = sext i32 %58 to i64
  br label %60

60:                                               ; preds = %86, %.preheader1
  %indvars.iv92 = phi i64 [ 0, %.preheader1 ], [ %indvars.iv.next93, %86 ]
  %exitcond94 = icmp eq i64 %indvars.iv92, 5
  br i1 %exitcond94, label %87, label %61

61:                                               ; preds = %60
  %62 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 %indvars.iv95, i64 %indvars.iv98, i64 %indvars.iv92, i64 %59
  %63 = load i32, i32* %62, align 4
  %64 = sext i32 %63 to i64
  %65 = getelementptr inbounds double, double* %tmor, i64 %64
  %66 = bitcast double* %65 to i64*
  %67 = load i64, i64* %66, align 8
  %68 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv98, i64 %indvars.iv92, i64 %59
  %69 = bitcast double* %68 to i64*
  store i64 %67, i64* %69, align 8
  br label %70

70:                                               ; preds = %85, %61
  %indvars.iv89 = phi i64 [ %indvars.iv.next90, %85 ], [ 1, %61 ]
  %exitcond91 = icmp eq i64 %indvars.iv89, 4
  br i1 %exitcond91, label %86, label %.preheader

.preheader:                                       ; preds = %70
  %71 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv98, i64 %indvars.iv92, i64 %indvars.iv89
  %72 = add nsw i64 %indvars.iv89, -1
  %.promoted = load double, double* %71, align 8
  br label %73

73:                                               ; preds = %75, %.preheader
  %indvars.iv86 = phi i64 [ 0, %.preheader ], [ %indvars.iv.next87, %75 ]
  %74 = phi double [ %.promoted, %.preheader ], [ %84, %75 ]
  %exitcond88 = icmp eq i64 %indvars.iv86, 5
  br i1 %exitcond88, label %85, label %75

75:                                               ; preds = %73
  %76 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 %indvars.iv95, i64 %indvars.iv98, i64 %indvars.iv92, i64 %indvars.iv86
  %77 = load i32, i32* %76, align 4
  %78 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv95, i64 %indvars.iv86, i64 %72
  %79 = load double, double* %78, align 8
  %80 = sext i32 %77 to i64
  %81 = getelementptr inbounds double, double* %tmor, i64 %80
  %82 = load double, double* %81, align 8
  %83 = fmul double %79, %82
  %84 = fadd double %74, %83
  %indvars.iv.next87 = add nuw nsw i64 %indvars.iv86, 1
  br label %73

85:                                               ; preds = %73
  store double %74, double* %71, align 8
  %indvars.iv.next90 = add nuw nsw i64 %indvars.iv89, 1
  br label %70

86:                                               ; preds = %70
  %indvars.iv.next93 = add nuw nsw i64 %indvars.iv92, 1
  br label %60

87:                                               ; preds = %60
  %indvars.iv.next96 = add nuw nsw i64 %indvars.iv95, 1
  br label %.preheader9

88:                                               ; preds = %.preheader9
  %indvars.iv.next99 = add nuw nsw i64 %indvars.iv98, 1
  br label %56

.preheader11:                                     ; preds = %155, %56
  %indvars.iv123 = phi i64 [ %indvars.iv.next124, %155 ], [ 0, %56 ]
  %exitcond126 = icmp eq i64 %indvars.iv123, 2
  br i1 %exitcond126, label %.loopexit, label %.preheader8

.preheader8:                                      ; preds = %106, %.preheader11
  %indvars.iv105 = phi i64 [ %indvars.iv.next106, %106 ], [ 1, %.preheader11 ]
  %exitcond107 = icmp eq i64 %indvars.iv105, 4
  br i1 %exitcond107, label %.preheader7, label %90

.preheader7:                                      ; preds = %.preheader8
  %89 = getelementptr inbounds [2 x i32], [2 x i32]* @v_end, i64 0, i64 %indvars.iv123
  br label %107

90:                                               ; preds = %.preheader8
  %91 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 %indvars.iv105, i64 0
  %92 = load i32, i32* %91, align 4
  %93 = sext i32 %92 to i64
  %94 = getelementptr inbounds double, double* %tx, i64 %93
  %95 = add nsw i64 %indvars.iv105, -1
  br label %96

96:                                               ; preds = %97, %90
  %indvars.iv102 = phi i64 [ %indvars.iv.next103, %97 ], [ 0, %90 ]
  %exitcond104 = icmp eq i64 %indvars.iv102, 5
  br i1 %exitcond104, label %106, label %97

97:                                               ; preds = %96
  %98 = load double, double* %94, align 8
  %99 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv123, i64 %indvars.iv102, i64 %95
  %100 = load double, double* %99, align 8
  %101 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv123, i64 %indvars.iv102, i64 0
  %102 = load double, double* %101, align 8
  %103 = fmul double %100, %102
  %104 = fmul double %103, 5.000000e-01
  %105 = fadd double %98, %104
  store double %105, double* %94, align 8
  %indvars.iv.next103 = add nuw nsw i64 %indvars.iv102, 1
  br label %96

106:                                              ; preds = %96
  %indvars.iv.next106 = add nuw nsw i64 %indvars.iv105, 1
  br label %.preheader8

107:                                              ; preds = %137, %.preheader7
  %indvars.iv114 = phi i64 [ 1, %.preheader7 ], [ %indvars.iv.next115, %137 ]
  %exitcond116 = icmp eq i64 %indvars.iv114, 4
  br i1 %exitcond116, label %.preheader6, label %108

108:                                              ; preds = %107
  %109 = load i32, i32* %89, align 4
  %110 = sext i32 %109 to i64
  %111 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 %110, i64 %indvars.iv114
  %112 = load i32, i32* %111, align 4
  %113 = sext i32 %112 to i64
  %114 = getelementptr inbounds double, double* %tx, i64 %113
  %115 = load double, double* %114, align 8
  %116 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv123, i64 %110, i64 %indvars.iv114
  %117 = load double, double* %116, align 8
  %118 = fmul double %117, 5.000000e-01
  %119 = fadd double %115, %118
  store double %119, double* %114, align 8
  br label %120

120:                                              ; preds = %136, %108
  %indvars.iv111 = phi i64 [ %indvars.iv.next112, %136 ], [ 1, %108 ]
  %exitcond113 = icmp eq i64 %indvars.iv111, 4
  br i1 %exitcond113, label %137, label %121

121:                                              ; preds = %120
  %122 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 %indvars.iv111, i64 %indvars.iv114
  %123 = load i32, i32* %122, align 4
  %124 = sext i32 %123 to i64
  %125 = getelementptr inbounds double, double* %tx, i64 %124
  %126 = add nsw i64 %indvars.iv111, -1
  br label %127

127:                                              ; preds = %128, %121
  %indvars.iv108 = phi i64 [ %indvars.iv.next109, %128 ], [ 0, %121 ]
  %exitcond110 = icmp eq i64 %indvars.iv108, 5
  br i1 %exitcond110, label %136, label %128

128:                                              ; preds = %127
  %129 = load double, double* %125, align 8
  %130 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv123, i64 %indvars.iv108, i64 %126
  %131 = load double, double* %130, align 8
  %132 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv123, i64 %indvars.iv108, i64 %indvars.iv114
  %133 = load double, double* %132, align 8
  %134 = fmul double %131, %133
  %135 = fadd double %129, %134
  store double %135, double* %125, align 8
  %indvars.iv.next109 = add nuw nsw i64 %indvars.iv108, 1
  br label %127

136:                                              ; preds = %127
  %indvars.iv.next112 = add nuw nsw i64 %indvars.iv111, 1
  br label %120

137:                                              ; preds = %120
  %indvars.iv.next115 = add nuw nsw i64 %indvars.iv114, 1
  br label %107

.preheader6:                                      ; preds = %154, %107
  %indvars.iv120 = phi i64 [ %indvars.iv.next121, %154 ], [ 1, %107 ]
  %exitcond122 = icmp eq i64 %indvars.iv120, 4
  br i1 %exitcond122, label %155, label %138

138:                                              ; preds = %.preheader6
  %139 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 %indvars.iv120, i64 4
  %140 = load i32, i32* %139, align 4
  %141 = sext i32 %140 to i64
  %142 = getelementptr inbounds double, double* %tx, i64 %141
  %143 = add nsw i64 %indvars.iv120, -1
  br label %144

144:                                              ; preds = %145, %138
  %indvars.iv117 = phi i64 [ %indvars.iv.next118, %145 ], [ 0, %138 ]
  %exitcond119 = icmp eq i64 %indvars.iv117, 5
  br i1 %exitcond119, label %154, label %145

145:                                              ; preds = %144
  %146 = load double, double* %142, align 8
  %147 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv123, i64 %indvars.iv117, i64 %143
  %148 = load double, double* %147, align 8
  %149 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %tmp, i64 0, i64 %indvars.iv123, i64 %indvars.iv117, i64 4
  %150 = load double, double* %149, align 8
  %151 = fmul double %148, %150
  %152 = fmul double %151, 5.000000e-01
  %153 = fadd double %146, %152
  store double %153, double* %142, align 8
  %indvars.iv.next118 = add nuw nsw i64 %indvars.iv117, 1
  br label %144

154:                                              ; preds = %144
  %indvars.iv.next121 = add nuw nsw i64 %indvars.iv120, 1
  br label %.preheader6

155:                                              ; preds = %.preheader6
  %indvars.iv.next124 = add nuw nsw i64 %indvars.iv123, 1
  br label %.preheader11

.preheader28:                                     ; preds = %168, %7
  %indvars.iv35 = phi i64 [ %indvars.iv.next36, %168 ], [ 1, %7 ]
  %exitcond37 = icmp eq i64 %indvars.iv35, 4
  br i1 %exitcond37, label %169, label %.preheader10

.preheader10:                                     ; preds = %156, %.preheader28
  %indvars.iv = phi i64 [ %indvars.iv.next, %156 ], [ 1, %.preheader28 ]
  %exitcond = icmp eq i64 %indvars.iv, 4
  br i1 %exitcond, label %168, label %156

156:                                              ; preds = %.preheader10
  %157 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 %indvars.iv35, i64 %indvars.iv
  %158 = load i32, i32* %157, align 4
  %159 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 0, i64 %indvars.iv35, i64 %indvars.iv
  %160 = load i32, i32* %159, align 4
  %161 = sext i32 %160 to i64
  %162 = getelementptr inbounds double, double* %tmor, i64 %161
  %163 = bitcast double* %162 to i64*
  %164 = load i64, i64* %163, align 8
  %165 = sext i32 %158 to i64
  %166 = getelementptr inbounds double, double* %tx, i64 %165
  %167 = bitcast double* %166 to i64*
  store i64 %164, i64* %167, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  br label %.preheader10

168:                                              ; preds = %.preheader10
  %indvars.iv.next36 = add nuw nsw i64 %indvars.iv35, 1
  br label %.preheader28

169:                                              ; preds = %.preheader28
  %170 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 0, i64 0, i64 4
  %171 = load i32, i32* %170, align 16
  %172 = icmp eq i32 %171, -1
  br i1 %172, label %.preheader24, label %.preheader26

.preheader26:                                     ; preds = %193, %169
  %indvars.iv44 = phi i64 [ %indvars.iv.next45, %193 ], [ 1, %169 ]
  %exitcond46 = icmp eq i64 %indvars.iv44, 4
  br i1 %exitcond46, label %.loopexit25, label %173

173:                                              ; preds = %.preheader26
  %174 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 %indvars.iv44
  %175 = load i32, i32* %174, align 4
  %176 = sext i32 %175 to i64
  %177 = getelementptr inbounds double, double* %tx, i64 %176
  %178 = add nsw i64 %indvars.iv44, -1
  br label %179

179:                                              ; preds = %192, %173
  %indvars.iv41 = phi i64 [ %indvars.iv.next42, %192 ], [ 0, %173 ]
  %exitcond43 = icmp eq i64 %indvars.iv41, 2
  br i1 %exitcond43, label %193, label %.preheader5

.preheader5:                                      ; preds = %180, %179
  %indvars.iv38 = phi i64 [ %indvars.iv.next39, %180 ], [ 0, %179 ]
  %exitcond40 = icmp eq i64 %indvars.iv38, 5
  br i1 %exitcond40, label %192, label %180

180:                                              ; preds = %.preheader5
  %181 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 %indvars.iv41, i64 0, i64 0, i64 %indvars.iv38
  %182 = load i32, i32* %181, align 4
  %183 = load double, double* %177, align 8
  %184 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv41, i64 %indvars.iv38, i64 %178
  %185 = load double, double* %184, align 8
  %186 = sext i32 %182 to i64
  %187 = getelementptr inbounds double, double* %tmor, i64 %186
  %188 = load double, double* %187, align 8
  %189 = fmul double %185, %188
  %190 = fmul double %189, 5.000000e-01
  %191 = fadd double %183, %190
  store double %191, double* %177, align 8
  %indvars.iv.next39 = add nuw nsw i64 %indvars.iv38, 1
  br label %.preheader5

192:                                              ; preds = %.preheader5
  %indvars.iv.next42 = add nuw nsw i64 %indvars.iv41, 1
  br label %179

193:                                              ; preds = %179
  %indvars.iv.next45 = add nuw nsw i64 %indvars.iv44, 1
  br label %.preheader26

.preheader24:                                     ; preds = %194, %169
  %indvars.iv47 = phi i64 [ %indvars.iv.next48, %194 ], [ 1, %169 ]
  %exitcond49 = icmp eq i64 %indvars.iv47, 4
  br i1 %exitcond49, label %.loopexit25, label %194

194:                                              ; preds = %.preheader24
  %195 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 %indvars.iv47
  %196 = load i32, i32* %195, align 4
  %197 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 0, i64 0, i64 %indvars.iv47
  %198 = load i32, i32* %197, align 4
  %199 = sext i32 %198 to i64
  %200 = getelementptr inbounds double, double* %tmor, i64 %199
  %201 = bitcast double* %200 to i64*
  %202 = load i64, i64* %201, align 8
  %203 = sext i32 %196 to i64
  %204 = getelementptr inbounds double, double* %tx, i64 %203
  %205 = bitcast double* %204 to i64*
  store i64 %202, i64* %205, align 8
  %indvars.iv.next48 = add nuw nsw i64 %indvars.iv47, 1
  br label %.preheader24

.loopexit25:                                      ; preds = %.preheader24, %.preheader26
  %206 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 1, i64 0, i64 1, i64 4
  %207 = load i32, i32* %206, align 4
  %208 = icmp eq i32 %207, -1
  br i1 %208, label %.preheader20, label %.preheader22

.preheader22:                                     ; preds = %229, %.loopexit25
  %indvars.iv56 = phi i64 [ %indvars.iv.next57, %229 ], [ 1, %.loopexit25 ]
  %exitcond58 = icmp eq i64 %indvars.iv56, 4
  br i1 %exitcond58, label %.loopexit21, label %209

209:                                              ; preds = %.preheader22
  %210 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 %indvars.iv56, i64 4
  %211 = load i32, i32* %210, align 4
  %212 = sext i32 %211 to i64
  %213 = getelementptr inbounds double, double* %tx, i64 %212
  %214 = add nsw i64 %indvars.iv56, -1
  br label %215

215:                                              ; preds = %228, %209
  %indvars.iv53 = phi i64 [ %indvars.iv.next54, %228 ], [ 0, %209 ]
  %exitcond55 = icmp eq i64 %indvars.iv53, 2
  br i1 %exitcond55, label %229, label %.preheader4

.preheader4:                                      ; preds = %216, %215
  %indvars.iv50 = phi i64 [ %indvars.iv.next51, %216 ], [ 0, %215 ]
  %exitcond52 = icmp eq i64 %indvars.iv50, 5
  br i1 %exitcond52, label %228, label %216

216:                                              ; preds = %.preheader4
  %217 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 1, i64 %indvars.iv53, i64 %indvars.iv50, i64 4
  %218 = load i32, i32* %217, align 4
  %219 = load double, double* %213, align 8
  %220 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv53, i64 %indvars.iv50, i64 %214
  %221 = load double, double* %220, align 8
  %222 = sext i32 %218 to i64
  %223 = getelementptr inbounds double, double* %tmor, i64 %222
  %224 = load double, double* %223, align 8
  %225 = fmul double %221, %224
  %226 = fmul double %225, 5.000000e-01
  %227 = fadd double %219, %226
  store double %227, double* %213, align 8
  %indvars.iv.next51 = add nuw nsw i64 %indvars.iv50, 1
  br label %.preheader4

228:                                              ; preds = %.preheader4
  %indvars.iv.next54 = add nuw nsw i64 %indvars.iv53, 1
  br label %215

229:                                              ; preds = %215
  %indvars.iv.next57 = add nuw nsw i64 %indvars.iv56, 1
  br label %.preheader22

.preheader20:                                     ; preds = %230, %.loopexit25
  %indvars.iv59 = phi i64 [ %indvars.iv.next60, %230 ], [ 1, %.loopexit25 ]
  %exitcond61 = icmp eq i64 %indvars.iv59, 4
  br i1 %exitcond61, label %.loopexit21, label %230

230:                                              ; preds = %.preheader20
  %231 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 %indvars.iv59, i64 4
  %232 = load i32, i32* %231, align 4
  %233 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 0, i64 %indvars.iv59, i64 4
  %234 = load i32, i32* %233, align 4
  %235 = sext i32 %234 to i64
  %236 = getelementptr inbounds double, double* %tmor, i64 %235
  %237 = bitcast double* %236 to i64*
  %238 = load i64, i64* %237, align 8
  %239 = sext i32 %232 to i64
  %240 = getelementptr inbounds double, double* %tx, i64 %239
  %241 = bitcast double* %240 to i64*
  store i64 %238, i64* %241, align 8
  %indvars.iv.next60 = add nuw nsw i64 %indvars.iv59, 1
  br label %.preheader20

.loopexit21:                                      ; preds = %.preheader20, %.preheader22
  %242 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 1, i64 4, i64 1
  %243 = load i32, i32* %242, align 4
  %244 = icmp eq i32 %243, -1
  br i1 %244, label %.preheader16, label %.preheader18

.preheader18:                                     ; preds = %265, %.loopexit21
  %indvars.iv68 = phi i64 [ %indvars.iv.next69, %265 ], [ 1, %.loopexit21 ]
  %exitcond70 = icmp eq i64 %indvars.iv68, 4
  br i1 %exitcond70, label %.loopexit17, label %245

245:                                              ; preds = %.preheader18
  %246 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 4, i64 %indvars.iv68
  %247 = load i32, i32* %246, align 4
  %248 = sext i32 %247 to i64
  %249 = getelementptr inbounds double, double* %tx, i64 %248
  %250 = add nsw i64 %indvars.iv68, -1
  br label %251

251:                                              ; preds = %264, %245
  %indvars.iv65 = phi i64 [ %indvars.iv.next66, %264 ], [ 0, %245 ]
  %exitcond67 = icmp eq i64 %indvars.iv65, 2
  br i1 %exitcond67, label %265, label %.preheader3

.preheader3:                                      ; preds = %252, %251
  %indvars.iv62 = phi i64 [ %indvars.iv.next63, %252 ], [ 0, %251 ]
  %exitcond64 = icmp eq i64 %indvars.iv62, 5
  br i1 %exitcond64, label %264, label %252

252:                                              ; preds = %.preheader3
  %253 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 %indvars.iv65, i64 1, i64 4, i64 %indvars.iv62
  %254 = load i32, i32* %253, align 4
  %255 = load double, double* %249, align 8
  %256 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv65, i64 %indvars.iv62, i64 %250
  %257 = load double, double* %256, align 8
  %258 = sext i32 %254 to i64
  %259 = getelementptr inbounds double, double* %tmor, i64 %258
  %260 = load double, double* %259, align 8
  %261 = fmul double %257, %260
  %262 = fmul double %261, 5.000000e-01
  %263 = fadd double %255, %262
  store double %263, double* %249, align 8
  %indvars.iv.next63 = add nuw nsw i64 %indvars.iv62, 1
  br label %.preheader3

264:                                              ; preds = %.preheader3
  %indvars.iv.next66 = add nuw nsw i64 %indvars.iv65, 1
  br label %251

265:                                              ; preds = %251
  %indvars.iv.next69 = add nuw nsw i64 %indvars.iv68, 1
  br label %.preheader18

.preheader16:                                     ; preds = %266, %.loopexit21
  %indvars.iv71 = phi i64 [ %indvars.iv.next72, %266 ], [ 1, %.loopexit21 ]
  %exitcond73 = icmp eq i64 %indvars.iv71, 4
  br i1 %exitcond73, label %.loopexit17, label %266

266:                                              ; preds = %.preheader16
  %267 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 4, i64 %indvars.iv71
  %268 = load i32, i32* %267, align 4
  %269 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 0, i64 4, i64 %indvars.iv71
  %270 = load i32, i32* %269, align 4
  %271 = sext i32 %270 to i64
  %272 = getelementptr inbounds double, double* %tmor, i64 %271
  %273 = bitcast double* %272 to i64*
  %274 = load i64, i64* %273, align 8
  %275 = sext i32 %268 to i64
  %276 = getelementptr inbounds double, double* %tx, i64 %275
  %277 = bitcast double* %276 to i64*
  store i64 %274, i64* %277, align 8
  %indvars.iv.next72 = add nuw nsw i64 %indvars.iv71, 1
  br label %.preheader16

.loopexit17:                                      ; preds = %.preheader16, %.preheader18
  %278 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 0, i64 4, i64 0
  %279 = load i32, i32* %278, align 16
  %280 = icmp eq i32 %279, -1
  br i1 %280, label %.preheader12, label %.preheader14

.preheader14:                                     ; preds = %301, %.loopexit17
  %indvars.iv80 = phi i64 [ %indvars.iv.next81, %301 ], [ 1, %.loopexit17 ]
  %exitcond82 = icmp eq i64 %indvars.iv80, 4
  br i1 %exitcond82, label %.loopexit, label %281

281:                                              ; preds = %.preheader14
  %282 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 %indvars.iv80, i64 0
  %283 = load i32, i32* %282, align 4
  %284 = sext i32 %283 to i64
  %285 = getelementptr inbounds double, double* %tx, i64 %284
  %286 = add nsw i64 %indvars.iv80, -1
  br label %287

287:                                              ; preds = %300, %281
  %indvars.iv77 = phi i64 [ %indvars.iv.next78, %300 ], [ 0, %281 ]
  %exitcond79 = icmp eq i64 %indvars.iv77, 2
  br i1 %exitcond79, label %301, label %.preheader2

.preheader2:                                      ; preds = %288, %287
  %indvars.iv74 = phi i64 [ %indvars.iv.next75, %288 ], [ 0, %287 ]
  %exitcond76 = icmp eq i64 %indvars.iv74, 5
  br i1 %exitcond76, label %300, label %288

288:                                              ; preds = %.preheader2
  %289 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 %indvars.iv77, i64 %indvars.iv74, i64 0
  %290 = load i32, i32* %289, align 4
  %291 = load double, double* %285, align 8
  %292 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv77, i64 %indvars.iv74, i64 %286
  %293 = load double, double* %292, align 8
  %294 = sext i32 %290 to i64
  %295 = getelementptr inbounds double, double* %tmor, i64 %294
  %296 = load double, double* %295, align 8
  %297 = fmul double %293, %296
  %298 = fmul double %297, 5.000000e-01
  %299 = fadd double %291, %298
  store double %299, double* %285, align 8
  %indvars.iv.next75 = add nuw nsw i64 %indvars.iv74, 1
  br label %.preheader2

300:                                              ; preds = %.preheader2
  %indvars.iv.next78 = add nuw nsw i64 %indvars.iv77, 1
  br label %287

301:                                              ; preds = %287
  %indvars.iv.next81 = add nuw nsw i64 %indvars.iv80, 1
  br label %.preheader14

.preheader12:                                     ; preds = %302, %.loopexit17
  %indvars.iv83 = phi i64 [ %indvars.iv.next84, %302 ], [ 1, %.loopexit17 ]
  %exitcond85 = icmp eq i64 %indvars.iv83, 4
  br i1 %exitcond85, label %.loopexit, label %302

302:                                              ; preds = %.preheader12
  %303 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 %indvars.iv83, i64 0
  %304 = load i32, i32* %303, align 4
  %305 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv130, i64 %indvars.iv127, i64 0, i64 0, i64 %indvars.iv83, i64 0
  %306 = load i32, i32* %305, align 4
  %307 = sext i32 %306 to i64
  %308 = getelementptr inbounds double, double* %tmor, i64 %307
  %309 = bitcast double* %308 to i64*
  %310 = load i64, i64* %309, align 8
  %311 = sext i32 %304 to i64
  %312 = getelementptr inbounds double, double* %tx, i64 %311
  %313 = bitcast double* %312 to i64*
  store i64 %310, i64* %313, align 8
  %indvars.iv.next84 = add nuw nsw i64 %indvars.iv83, 1
  br label %.preheader12

.loopexit:                                        ; preds = %.preheader12, %.preheader14, %.preheader11
  %indvars.iv.next128 = add nuw nsw i64 %indvars.iv127, 1
  br label %.preheader29

314:                                              ; preds = %.preheader29
  %indvars.iv.next131 = add nuw nsw i64 %indvars.iv130, 1
  br label %3

315:                                              ; preds = %3
  ret void
}

declare void @col2(double*, double*, i32) local_unnamed_addr #1

declare void @r_init(double*, i32, double) local_unnamed_addr #1

; Function Attrs: nounwind uwtable
define void @transfb(double* %tmor, double* nocapture readonly %tx) local_unnamed_addr #0 {
  %temp = alloca [2 x [5 x [5 x double]]], align 16
  %top = alloca [2 x [5 x double]], align 16
  %1 = load i32, i32* @nmor, align 4
  tail call void @r_init(double* %tmor, i32 %1, double 0.000000e+00) #3
  %2 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 0, i64 0, i64 0
  br label %3

3:                                                ; preds = %336, %0
  %indvars.iv145 = phi i64 [ %indvars.iv.next146, %336 ], [ 0, %0 ]
  %4 = load i32, i32* @nelt, align 4
  %5 = sext i32 %4 to i64
  %6 = icmp slt i64 %indvars.iv145, %5
  br i1 %6, label %.preheader32, label %337

.preheader32:                                     ; preds = %.loopexit, %3
  %indvars.iv142 = phi i64 [ %indvars.iv.next143, %.loopexit ], [ 0, %3 ]
  %exitcond144 = icmp eq i64 %indvars.iv142, 6
  br i1 %exitcond144, label %336, label %7

7:                                                ; preds = %.preheader32
  %8 = getelementptr inbounds [8800 x [6 x i32]], [8800 x [6 x i32]]* @cbc, i64 0, i64 %indvars.iv145, i64 %indvars.iv142
  %9 = load i32, i32* %8, align 4
  %10 = icmp eq i32 %9, 3
  %11 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 0
  %12 = load i32, i32* %11, align 4
  %13 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 4
  %14 = load i32, i32* %13, align 4
  %15 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 4, i64 0
  %16 = load i32, i32* %15, align 4
  %17 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 4, i64 4
  %18 = load i32, i32* %17, align 4
  %19 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 0, i64 0, i64 0
  %20 = load i32, i32* %19, align 16
  %21 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 1, i64 0, i64 0, i64 4
  %22 = load i32, i32* %21, align 8
  %23 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 1, i64 4, i64 0
  %24 = load i32, i32* %23, align 4
  %25 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 1, i64 1, i64 4, i64 4
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
  br i1 %10, label %59, label %.preheader31

59:                                               ; preds = %7
  call void @r_init(double* nonnull %2, i32 50, double 0.000000e+00) #3
  br label %60

60:                                               ; preds = %105, %59
  %indvars.iv109 = phi i64 [ %indvars.iv.next110, %105 ], [ 0, %59 ]
  %indvars.iv107 = phi i64 [ %indvars.iv.next108, %105 ], [ 5, %59 ]
  %indvars.iv97 = phi i64 [ %indvars.iv.next98, %105 ], [ 1, %59 ]
  %exitcond112 = icmp eq i64 %indvars.iv109, 2
  br i1 %exitcond112, label %.preheader14, label %.preheader8

.preheader8:                                      ; preds = %60
  %61 = getelementptr inbounds [2 x i32], [2 x i32]* @v_end, i64 0, i64 %indvars.iv109
  %62 = load i32, i32* %61, align 4
  %63 = sext i32 %62 to i64
  br label %64

64:                                               ; preds = %104, %.preheader8
  %indvars.iv104 = phi i64 [ 0, %.preheader8 ], [ %indvars.iv.next105, %104 ]
  %exitcond106 = icmp eq i64 %indvars.iv104, 5
  br i1 %exitcond106, label %105, label %65

65:                                               ; preds = %64
  %66 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %63, i64 %indvars.iv104
  %67 = load i32, i32* %66, align 4
  %68 = sext i32 %67 to i64
  %69 = getelementptr inbounds double, double* %tx, i64 %68
  %70 = bitcast double* %69 to i64*
  %71 = load i64, i64* %70, align 8
  %72 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv109, i64 %63, i64 %indvars.iv104
  %73 = bitcast double* %72 to i64*
  store i64 %71, i64* %73, align 8
  br label %74

74:                                               ; preds = %75, %65
  %indvars.iv91 = phi i64 [ %indvars.iv.next92, %75 ], [ 1, %65 ]
  %tmp.0 = phi double [ %85, %75 ], [ 0.000000e+00, %65 ]
  %exitcond93 = icmp eq i64 %indvars.iv91, 4
  br i1 %exitcond93, label %86, label %75

75:                                               ; preds = %74
  %76 = add nsw i64 %indvars.iv91, -1
  %77 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv109, i64 %63, i64 %76
  %78 = load double, double* %77, align 8
  %79 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %indvars.iv91, i64 %indvars.iv104
  %80 = load i32, i32* %79, align 4
  %81 = sext i32 %80 to i64
  %82 = getelementptr inbounds double, double* %tx, i64 %81
  %83 = load double, double* %82, align 8
  %84 = fmul double %78, %83
  %85 = fadd double %tmp.0, %84
  %indvars.iv.next92 = add nuw nsw i64 %indvars.iv91, 1
  br label %74

86:                                               ; preds = %74
  %87 = getelementptr inbounds [2 x [5 x double]], [2 x [5 x double]]* %top, i64 0, i64 %indvars.iv109, i64 %indvars.iv104
  store double %tmp.0, double* %87, align 8
  br label %88

88:                                               ; preds = %100, %86
  %indvars.iv99 = phi i64 [ %indvars.iv.next100, %100 ], [ %indvars.iv97, %86 ]
  %exitcond103 = icmp eq i64 %indvars.iv99, %indvars.iv107
  br i1 %exitcond103, label %104, label %.preheader2

.preheader2:                                      ; preds = %89, %88
  %indvars.iv94 = phi i64 [ %indvars.iv.next95, %89 ], [ 1, %88 ]
  %tmp.1 = phi double [ %99, %89 ], [ 0.000000e+00, %88 ]
  %exitcond96 = icmp eq i64 %indvars.iv94, 4
  br i1 %exitcond96, label %100, label %89

89:                                               ; preds = %.preheader2
  %90 = add nsw i64 %indvars.iv94, -1
  %91 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv109, i64 %indvars.iv99, i64 %90
  %92 = load double, double* %91, align 8
  %93 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %indvars.iv94, i64 %indvars.iv104
  %94 = load i32, i32* %93, align 4
  %95 = sext i32 %94 to i64
  %96 = getelementptr inbounds double, double* %tx, i64 %95
  %97 = load double, double* %96, align 8
  %98 = fmul double %92, %97
  %99 = fadd double %tmp.1, %98
  %indvars.iv.next95 = add nuw nsw i64 %indvars.iv94, 1
  br label %.preheader2

100:                                              ; preds = %.preheader2
  %101 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv109, i64 %indvars.iv99, i64 %indvars.iv104
  %102 = load double, double* %101, align 8
  %103 = fadd double %tmp.1, %102
  store double %103, double* %101, align 8
  %indvars.iv.next100 = add nsw i64 %indvars.iv99, 1
  br label %88

104:                                              ; preds = %88
  %indvars.iv.next105 = add nuw nsw i64 %indvars.iv104, 1
  br label %64

105:                                              ; preds = %64
  %indvars.iv.next110 = add nuw nsw i64 %indvars.iv109, 1
  %indvars.iv.next98 = add nsw i64 %indvars.iv97, -1
  %indvars.iv.next108 = add nsw i64 %indvars.iv107, -1
  br label %60

.preheader14:                                     ; preds = %177, %60
  %indvars.iv138 = phi i64 [ %indvars.iv.next139, %177 ], [ 0, %60 ]
  %indvars.iv136 = phi i64 [ %indvars.iv.next137, %177 ], [ 5, %60 ]
  %indvars.iv119 = phi i64 [ %indvars.iv.next120, %177 ], [ 1, %60 ]
  %exitcond141 = icmp eq i64 %indvars.iv138, 2
  br i1 %exitcond141, label %.loopexit, label %.preheader7

.preheader7:                                      ; preds = %.preheader14
  %106 = getelementptr inbounds [2 x i32], [2 x i32]* @v_end, i64 0, i64 %indvars.iv138
  br label %107

107:                                              ; preds = %176, %.preheader7
  %indvars.iv132 = phi i64 [ 0, %.preheader7 ], [ %indvars.iv.next133, %176 ]
  %exitcond135 = icmp eq i64 %indvars.iv132, 2
  br i1 %exitcond135, label %177, label %108

108:                                              ; preds = %107
  %109 = getelementptr inbounds [2 x i32], [2 x i32]* @v_end, i64 0, i64 %indvars.iv132
  br label %110

110:                                              ; preds = %139, %108
  %indvars.iv121 = phi i64 [ %indvars.iv.next122, %139 ], [ %indvars.iv119, %108 ]
  %exitcond125 = icmp eq i64 %indvars.iv121, %indvars.iv136
  br i1 %exitcond125, label %140, label %111

111:                                              ; preds = %110
  %112 = load i32, i32* %109, align 4
  %113 = sext i32 %112 to i64
  %114 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %indvars.iv132, i64 %indvars.iv138, i64 %indvars.iv121, i64 %113
  %115 = load i32, i32* %114, align 4
  %116 = sext i32 %115 to i64
  %117 = getelementptr inbounds double, double* %tmor, i64 %116
  %118 = load double, double* %117, align 8
  %119 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv138, i64 %indvars.iv121, i64 %113
  %120 = load double, double* %119, align 8
  %121 = fmul double %120, 5.000000e-01
  %122 = fadd double %118, %121
  store double %122, double* %117, align 8
  br label %123

123:                                              ; preds = %132, %111
  %indvars.iv116 = phi i64 [ %indvars.iv.next117, %132 ], [ 0, %111 ]
  %exitcond118 = icmp eq i64 %indvars.iv116, 5
  br i1 %exitcond118, label %139, label %.preheader

.preheader:                                       ; preds = %124, %123
  %indvars.iv113 = phi i64 [ %indvars.iv.next114, %124 ], [ 1, %123 ]
  %tmp.2 = phi double [ %131, %124 ], [ 0.000000e+00, %123 ]
  %exitcond115 = icmp eq i64 %indvars.iv113, 4
  br i1 %exitcond115, label %132, label %124

124:                                              ; preds = %.preheader
  %125 = add nsw i64 %indvars.iv113, -1
  %126 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv132, i64 %indvars.iv116, i64 %125
  %127 = load double, double* %126, align 8
  %128 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv138, i64 %indvars.iv121, i64 %indvars.iv113
  %129 = load double, double* %128, align 8
  %130 = fmul double %127, %129
  %131 = fadd double %tmp.2, %130
  %indvars.iv.next114 = add nuw nsw i64 %indvars.iv113, 1
  br label %.preheader

132:                                              ; preds = %.preheader
  %133 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %indvars.iv132, i64 %indvars.iv138, i64 %indvars.iv121, i64 %indvars.iv116
  %134 = load i32, i32* %133, align 4
  %135 = sext i32 %134 to i64
  %136 = getelementptr inbounds double, double* %tmor, i64 %135
  %137 = load double, double* %136, align 8
  %138 = fadd double %tmp.2, %137
  store double %138, double* %136, align 8
  %indvars.iv.next117 = add nuw nsw i64 %indvars.iv116, 1
  br label %123

139:                                              ; preds = %123
  %indvars.iv.next122 = add nsw i64 %indvars.iv121, 1
  br label %110

140:                                              ; preds = %110
  %141 = load i32, i32* %106, align 4
  %142 = load i32, i32* %109, align 4
  %143 = sext i32 %142 to i64
  %144 = sext i32 %141 to i64
  %145 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %indvars.iv132, i64 %indvars.iv138, i64 %144, i64 %143
  %146 = load i32, i32* %145, align 4
  %147 = sext i32 %146 to i64
  %148 = getelementptr inbounds double, double* %tmor, i64 %147
  %149 = load double, double* %148, align 8
  %150 = getelementptr inbounds [2 x [5 x double]], [2 x [5 x double]]* %top, i64 0, i64 %indvars.iv138, i64 %143
  %151 = load double, double* %150, align 8
  %152 = fmul double %151, 5.000000e-01
  %153 = fadd double %149, %152
  store double %153, double* %148, align 8
  br label %154

154:                                              ; preds = %167, %140
  %indvars.iv129 = phi i64 [ %indvars.iv.next130, %167 ], [ 0, %140 ]
  %exitcond131 = icmp eq i64 %indvars.iv129, 5
  br i1 %exitcond131, label %176, label %.preheader1

.preheader1:                                      ; preds = %155, %154
  %indvars.iv126 = phi i64 [ %indvars.iv.next127, %155 ], [ 1, %154 ]
  %tmp1.0 = phi double [ %162, %155 ], [ 0.000000e+00, %154 ]
  %tmp.3 = phi double [ %166, %155 ], [ 0.000000e+00, %154 ]
  %exitcond128 = icmp eq i64 %indvars.iv126, 4
  br i1 %exitcond128, label %167, label %155

155:                                              ; preds = %.preheader1
  %156 = add nsw i64 %indvars.iv126, -1
  %157 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv132, i64 %indvars.iv129, i64 %156
  %158 = load double, double* %157, align 8
  %159 = getelementptr inbounds [2 x [5 x double]], [2 x [5 x double]]* %top, i64 0, i64 %indvars.iv138, i64 %indvars.iv126
  %160 = load double, double* %159, align 8
  %161 = fmul double %158, %160
  %162 = fadd double %tmp1.0, %161
  %163 = getelementptr inbounds [2 x [5 x [5 x double]]], [2 x [5 x [5 x double]]]* %temp, i64 0, i64 %indvars.iv138, i64 %144, i64 %indvars.iv126
  %164 = load double, double* %163, align 8
  %165 = fmul double %158, %164
  %166 = fadd double %tmp.3, %165
  %indvars.iv.next127 = add nuw nsw i64 %indvars.iv126, 1
  br label %.preheader1

167:                                              ; preds = %.preheader1
  %168 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %indvars.iv132, i64 %indvars.iv138, i64 %144, i64 %indvars.iv129
  %169 = load i32, i32* %168, align 4
  %170 = sext i32 %169 to i64
  %171 = getelementptr inbounds double, double* %tmor, i64 %170
  %172 = load double, double* %171, align 8
  %173 = fmul double %tmp.3, 5.000000e-01
  %174 = fadd double %173, %172
  %175 = fadd double %tmp1.0, %174
  store double %175, double* %171, align 8
  %indvars.iv.next130 = add nuw nsw i64 %indvars.iv129, 1
  br label %154

176:                                              ; preds = %154
  %indvars.iv.next133 = add nuw nsw i64 %indvars.iv132, 1
  br label %107

177:                                              ; preds = %107
  %indvars.iv.next139 = add nuw nsw i64 %indvars.iv138, 1
  %indvars.iv.next120 = add nsw i64 %indvars.iv119, -1
  %indvars.iv.next137 = add nsw i64 %indvars.iv136, -1
  br label %.preheader14

.preheader31:                                     ; preds = %190, %7
  %indvars.iv40 = phi i64 [ %indvars.iv.next41, %190 ], [ 1, %7 ]
  %exitcond42 = icmp eq i64 %indvars.iv40, 4
  br i1 %exitcond42, label %191, label %.preheader13

.preheader13:                                     ; preds = %178, %.preheader31
  %indvars.iv = phi i64 [ %indvars.iv.next, %178 ], [ 1, %.preheader31 ]
  %exitcond = icmp eq i64 %indvars.iv, 4
  br i1 %exitcond, label %190, label %178

178:                                              ; preds = %.preheader13
  %179 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %indvars.iv40, i64 %indvars.iv
  %180 = load i32, i32* %179, align 4
  %181 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 0, i64 %indvars.iv40, i64 %indvars.iv
  %182 = load i32, i32* %181, align 4
  %183 = sext i32 %182 to i64
  %184 = getelementptr inbounds double, double* %tmor, i64 %183
  %185 = load double, double* %184, align 8
  %186 = sext i32 %180 to i64
  %187 = getelementptr inbounds double, double* %tx, i64 %186
  %188 = load double, double* %187, align 8
  %189 = fadd double %185, %188
  store double %189, double* %184, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  br label %.preheader13

190:                                              ; preds = %.preheader13
  %indvars.iv.next41 = add nuw nsw i64 %indvars.iv40, 1
  br label %.preheader31

191:                                              ; preds = %.preheader31
  %192 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 0, i64 0, i64 4
  %193 = load i32, i32* %192, align 16
  %194 = icmp eq i32 %193, -1
  br i1 %194, label %.preheader27, label %.preheader29

.preheader29:                                     ; preds = %214, %191
  %indvars.iv49 = phi i64 [ %indvars.iv.next50, %214 ], [ 0, %191 ]
  %exitcond51 = icmp eq i64 %indvars.iv49, 2
  br i1 %exitcond51, label %.loopexit28, label %.preheader12

.preheader12:                                     ; preds = %206, %.preheader29
  %indvars.iv46 = phi i64 [ %indvars.iv.next47, %206 ], [ 0, %.preheader29 ]
  %exitcond48 = icmp eq i64 %indvars.iv46, 5
  br i1 %exitcond48, label %214, label %.preheader6

.preheader6:                                      ; preds = %195, %.preheader12
  %indvars.iv43 = phi i64 [ %indvars.iv.next44, %195 ], [ 1, %.preheader12 ]
  %tmp.4 = phi double [ %205, %195 ], [ 0.000000e+00, %.preheader12 ]
  %exitcond45 = icmp eq i64 %indvars.iv43, 4
  br i1 %exitcond45, label %206, label %195

195:                                              ; preds = %.preheader6
  %196 = add nsw i64 %indvars.iv43, -1
  %197 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv49, i64 %indvars.iv46, i64 %196
  %198 = load double, double* %197, align 8
  %199 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 %indvars.iv43
  %200 = load i32, i32* %199, align 4
  %201 = sext i32 %200 to i64
  %202 = getelementptr inbounds double, double* %tx, i64 %201
  %203 = load double, double* %202, align 8
  %204 = fmul double %198, %203
  %205 = fadd double %tmp.4, %204
  %indvars.iv.next44 = add nuw nsw i64 %indvars.iv43, 1
  br label %.preheader6

206:                                              ; preds = %.preheader6
  %207 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %indvars.iv49, i64 0, i64 0, i64 %indvars.iv46
  %208 = load i32, i32* %207, align 4
  %209 = sext i32 %208 to i64
  %210 = getelementptr inbounds double, double* %tmor, i64 %209
  %211 = load double, double* %210, align 8
  %212 = fmul double %tmp.4, 5.000000e-01
  %213 = fadd double %212, %211
  store double %213, double* %210, align 8
  %indvars.iv.next47 = add nuw nsw i64 %indvars.iv46, 1
  br label %.preheader12

214:                                              ; preds = %.preheader12
  %indvars.iv.next50 = add nuw nsw i64 %indvars.iv49, 1
  br label %.preheader29

.preheader27:                                     ; preds = %215, %191
  %indvars.iv52 = phi i64 [ %indvars.iv.next53, %215 ], [ 1, %191 ]
  %exitcond54 = icmp eq i64 %indvars.iv52, 4
  br i1 %exitcond54, label %.loopexit28, label %215

215:                                              ; preds = %.preheader27
  %216 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 %indvars.iv52
  %217 = load i32, i32* %216, align 4
  %218 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 0, i64 0, i64 %indvars.iv52
  %219 = load i32, i32* %218, align 4
  %220 = sext i32 %219 to i64
  %221 = getelementptr inbounds double, double* %tmor, i64 %220
  %222 = load double, double* %221, align 8
  %223 = sext i32 %217 to i64
  %224 = getelementptr inbounds double, double* %tx, i64 %223
  %225 = load double, double* %224, align 8
  %226 = fmul double %225, 5.000000e-01
  %227 = fadd double %222, %226
  store double %227, double* %221, align 8
  %indvars.iv.next53 = add nuw nsw i64 %indvars.iv52, 1
  br label %.preheader27

.loopexit28:                                      ; preds = %.preheader27, %.preheader29
  %228 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 1, i64 0, i64 1, i64 4
  %229 = load i32, i32* %228, align 4
  %230 = icmp eq i32 %229, -1
  br i1 %230, label %.preheader23, label %.preheader25

.preheader25:                                     ; preds = %250, %.loopexit28
  %indvars.iv61 = phi i64 [ %indvars.iv.next62, %250 ], [ 0, %.loopexit28 ]
  %exitcond63 = icmp eq i64 %indvars.iv61, 2
  br i1 %exitcond63, label %.loopexit24, label %.preheader11

.preheader11:                                     ; preds = %242, %.preheader25
  %indvars.iv58 = phi i64 [ %indvars.iv.next59, %242 ], [ 0, %.preheader25 ]
  %exitcond60 = icmp eq i64 %indvars.iv58, 5
  br i1 %exitcond60, label %250, label %.preheader5

.preheader5:                                      ; preds = %231, %.preheader11
  %indvars.iv55 = phi i64 [ %indvars.iv.next56, %231 ], [ 1, %.preheader11 ]
  %tmp.5 = phi double [ %241, %231 ], [ 0.000000e+00, %.preheader11 ]
  %exitcond57 = icmp eq i64 %indvars.iv55, 4
  br i1 %exitcond57, label %242, label %231

231:                                              ; preds = %.preheader5
  %232 = add nsw i64 %indvars.iv55, -1
  %233 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv61, i64 %indvars.iv58, i64 %232
  %234 = load double, double* %233, align 8
  %235 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %indvars.iv55, i64 4
  %236 = load i32, i32* %235, align 4
  %237 = sext i32 %236 to i64
  %238 = getelementptr inbounds double, double* %tx, i64 %237
  %239 = load double, double* %238, align 8
  %240 = fmul double %234, %239
  %241 = fadd double %tmp.5, %240
  %indvars.iv.next56 = add nuw nsw i64 %indvars.iv55, 1
  br label %.preheader5

242:                                              ; preds = %.preheader5
  %243 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 1, i64 %indvars.iv61, i64 %indvars.iv58, i64 4
  %244 = load i32, i32* %243, align 4
  %245 = sext i32 %244 to i64
  %246 = getelementptr inbounds double, double* %tmor, i64 %245
  %247 = load double, double* %246, align 8
  %248 = fmul double %tmp.5, 5.000000e-01
  %249 = fadd double %248, %247
  store double %249, double* %246, align 8
  %indvars.iv.next59 = add nuw nsw i64 %indvars.iv58, 1
  br label %.preheader11

250:                                              ; preds = %.preheader11
  %indvars.iv.next62 = add nuw nsw i64 %indvars.iv61, 1
  br label %.preheader25

.preheader23:                                     ; preds = %251, %.loopexit28
  %indvars.iv64 = phi i64 [ %indvars.iv.next65, %251 ], [ 1, %.loopexit28 ]
  %exitcond66 = icmp eq i64 %indvars.iv64, 4
  br i1 %exitcond66, label %.loopexit24, label %251

251:                                              ; preds = %.preheader23
  %252 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %indvars.iv64, i64 4
  %253 = load i32, i32* %252, align 4
  %254 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 0, i64 %indvars.iv64, i64 4
  %255 = load i32, i32* %254, align 4
  %256 = sext i32 %255 to i64
  %257 = getelementptr inbounds double, double* %tmor, i64 %256
  %258 = load double, double* %257, align 8
  %259 = sext i32 %253 to i64
  %260 = getelementptr inbounds double, double* %tx, i64 %259
  %261 = load double, double* %260, align 8
  %262 = fmul double %261, 5.000000e-01
  %263 = fadd double %258, %262
  store double %263, double* %257, align 8
  %indvars.iv.next65 = add nuw nsw i64 %indvars.iv64, 1
  br label %.preheader23

.loopexit24:                                      ; preds = %.preheader23, %.preheader25
  %264 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 1, i64 4, i64 1
  %265 = load i32, i32* %264, align 4
  %266 = icmp eq i32 %265, -1
  br i1 %266, label %.preheader19, label %.preheader21

.preheader21:                                     ; preds = %286, %.loopexit24
  %indvars.iv73 = phi i64 [ %indvars.iv.next74, %286 ], [ 0, %.loopexit24 ]
  %exitcond75 = icmp eq i64 %indvars.iv73, 2
  br i1 %exitcond75, label %.loopexit20, label %.preheader10

.preheader10:                                     ; preds = %278, %.preheader21
  %indvars.iv70 = phi i64 [ %indvars.iv.next71, %278 ], [ 0, %.preheader21 ]
  %exitcond72 = icmp eq i64 %indvars.iv70, 5
  br i1 %exitcond72, label %286, label %.preheader4

.preheader4:                                      ; preds = %267, %.preheader10
  %indvars.iv67 = phi i64 [ %indvars.iv.next68, %267 ], [ 1, %.preheader10 ]
  %tmp.6 = phi double [ %277, %267 ], [ 0.000000e+00, %.preheader10 ]
  %exitcond69 = icmp eq i64 %indvars.iv67, 4
  br i1 %exitcond69, label %278, label %267

267:                                              ; preds = %.preheader4
  %268 = add nsw i64 %indvars.iv67, -1
  %269 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv73, i64 %indvars.iv70, i64 %268
  %270 = load double, double* %269, align 8
  %271 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 4, i64 %indvars.iv67
  %272 = load i32, i32* %271, align 4
  %273 = sext i32 %272 to i64
  %274 = getelementptr inbounds double, double* %tx, i64 %273
  %275 = load double, double* %274, align 8
  %276 = fmul double %270, %275
  %277 = fadd double %tmp.6, %276
  %indvars.iv.next68 = add nuw nsw i64 %indvars.iv67, 1
  br label %.preheader4

278:                                              ; preds = %.preheader4
  %279 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %indvars.iv73, i64 1, i64 4, i64 %indvars.iv70
  %280 = load i32, i32* %279, align 4
  %281 = sext i32 %280 to i64
  %282 = getelementptr inbounds double, double* %tmor, i64 %281
  %283 = load double, double* %282, align 8
  %284 = fmul double %tmp.6, 5.000000e-01
  %285 = fadd double %284, %283
  store double %285, double* %282, align 8
  %indvars.iv.next71 = add nuw nsw i64 %indvars.iv70, 1
  br label %.preheader10

286:                                              ; preds = %.preheader10
  %indvars.iv.next74 = add nuw nsw i64 %indvars.iv73, 1
  br label %.preheader21

.preheader19:                                     ; preds = %287, %.loopexit24
  %indvars.iv76 = phi i64 [ %indvars.iv.next77, %287 ], [ 1, %.loopexit24 ]
  %exitcond78 = icmp eq i64 %indvars.iv76, 4
  br i1 %exitcond78, label %.loopexit20, label %287

287:                                              ; preds = %.preheader19
  %288 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 4, i64 %indvars.iv76
  %289 = load i32, i32* %288, align 4
  %290 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 0, i64 4, i64 %indvars.iv76
  %291 = load i32, i32* %290, align 4
  %292 = sext i32 %291 to i64
  %293 = getelementptr inbounds double, double* %tmor, i64 %292
  %294 = load double, double* %293, align 8
  %295 = sext i32 %289 to i64
  %296 = getelementptr inbounds double, double* %tx, i64 %295
  %297 = load double, double* %296, align 8
  %298 = fmul double %297, 5.000000e-01
  %299 = fadd double %294, %298
  store double %299, double* %293, align 8
  %indvars.iv.next77 = add nuw nsw i64 %indvars.iv76, 1
  br label %.preheader19

.loopexit20:                                      ; preds = %.preheader19, %.preheader21
  %300 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 0, i64 4, i64 0
  %301 = load i32, i32* %300, align 16
  %302 = icmp eq i32 %301, -1
  br i1 %302, label %.preheader15, label %.preheader17

.preheader17:                                     ; preds = %322, %.loopexit20
  %indvars.iv85 = phi i64 [ %indvars.iv.next86, %322 ], [ 0, %.loopexit20 ]
  %exitcond87 = icmp eq i64 %indvars.iv85, 2
  br i1 %exitcond87, label %.loopexit, label %.preheader9

.preheader9:                                      ; preds = %314, %.preheader17
  %indvars.iv82 = phi i64 [ %indvars.iv.next83, %314 ], [ 0, %.preheader17 ]
  %exitcond84 = icmp eq i64 %indvars.iv82, 5
  br i1 %exitcond84, label %322, label %.preheader3

.preheader3:                                      ; preds = %303, %.preheader9
  %indvars.iv79 = phi i64 [ %indvars.iv.next80, %303 ], [ 1, %.preheader9 ]
  %tmp.7 = phi double [ %313, %303 ], [ 0.000000e+00, %.preheader9 ]
  %exitcond81 = icmp eq i64 %indvars.iv79, 4
  br i1 %exitcond81, label %314, label %303

303:                                              ; preds = %.preheader3
  %304 = add nsw i64 %indvars.iv79, -1
  %305 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 %indvars.iv85, i64 %indvars.iv82, i64 %304
  %306 = load double, double* %305, align 8
  %307 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %indvars.iv79, i64 0
  %308 = load i32, i32* %307, align 4
  %309 = sext i32 %308 to i64
  %310 = getelementptr inbounds double, double* %tx, i64 %309
  %311 = load double, double* %310, align 8
  %312 = fmul double %306, %311
  %313 = fadd double %tmp.7, %312
  %indvars.iv.next80 = add nuw nsw i64 %indvars.iv79, 1
  br label %.preheader3

314:                                              ; preds = %.preheader3
  %315 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 %indvars.iv85, i64 %indvars.iv82, i64 0
  %316 = load i32, i32* %315, align 4
  %317 = sext i32 %316 to i64
  %318 = getelementptr inbounds double, double* %tmor, i64 %317
  %319 = load double, double* %318, align 8
  %320 = fmul double %tmp.7, 5.000000e-01
  %321 = fadd double %320, %319
  store double %321, double* %318, align 8
  %indvars.iv.next83 = add nuw nsw i64 %indvars.iv82, 1
  br label %.preheader9

322:                                              ; preds = %.preheader9
  %indvars.iv.next86 = add nuw nsw i64 %indvars.iv85, 1
  br label %.preheader17

.preheader15:                                     ; preds = %323, %.loopexit20
  %indvars.iv88 = phi i64 [ %indvars.iv.next89, %323 ], [ 1, %.loopexit20 ]
  %exitcond90 = icmp eq i64 %indvars.iv88, 4
  br i1 %exitcond90, label %.loopexit, label %323

323:                                              ; preds = %.preheader15
  %324 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 %indvars.iv88, i64 0
  %325 = load i32, i32* %324, align 4
  %326 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv145, i64 %indvars.iv142, i64 0, i64 0, i64 %indvars.iv88, i64 0
  %327 = load i32, i32* %326, align 4
  %328 = sext i32 %327 to i64
  %329 = getelementptr inbounds double, double* %tmor, i64 %328
  %330 = load double, double* %329, align 8
  %331 = sext i32 %325 to i64
  %332 = getelementptr inbounds double, double* %tx, i64 %331
  %333 = load double, double* %332, align 8
  %334 = fmul double %333, 5.000000e-01
  %335 = fadd double %330, %334
  store double %335, double* %329, align 8
  %indvars.iv.next89 = add nuw nsw i64 %indvars.iv88, 1
  br label %.preheader15

.loopexit:                                        ; preds = %.preheader15, %.preheader17, %.preheader14
  %indvars.iv.next143 = add nuw nsw i64 %indvars.iv142, 1
  br label %.preheader32

336:                                              ; preds = %.preheader32
  %indvars.iv.next146 = add nuw nsw i64 %indvars.iv145, 1
  br label %3

337:                                              ; preds = %3
  ret void
}

; Function Attrs: nofree norecurse nounwind uwtable
define void @transfb_cor_e(i32 %n, double* nocapture %tmor, [5 x [5 x double]]* nocapture readonly %tx) local_unnamed_addr #2 {
  %1 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 0
  %2 = load double, double* %1, align 8
  br label %3

3:                                                ; preds = %4, %0
  %indvars.iv6 = phi i64 [ %indvars.iv.next7, %4 ], [ 1, %0 ]
  %tmp.0 = phi double [ %11, %4 ], [ %2, %0 ]
  %exitcond8 = icmp eq i64 %indvars.iv6, 4
  br i1 %exitcond8, label %12, label %4

4:                                                ; preds = %3
  %5 = add nsw i64 %indvars.iv6, -1
  %6 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %5
  %7 = load double, double* %6, align 8
  %8 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 %indvars.iv6
  %9 = load double, double* %8, align 8
  %10 = fmul double %7, %9
  %11 = fadd double %tmp.0, %10
  %indvars.iv.next7 = add nuw nsw i64 %indvars.iv6, 1
  br label %3

12:                                               ; preds = %3
  %13 = icmp sgt i32 %n, 1
  br i1 %13, label %.preheader2, label %.thread

.preheader2:                                      ; preds = %14, %12
  %indvars.iv3 = phi i64 [ %indvars.iv.next4, %14 ], [ 1, %12 ]
  %tmp.1 = phi double [ %21, %14 ], [ %tmp.0, %12 ]
  %exitcond5 = icmp eq i64 %indvars.iv3, 4
  br i1 %exitcond5, label %22, label %14

14:                                               ; preds = %.preheader2
  %15 = add nsw i64 %indvars.iv3, -1
  %16 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %15
  %17 = load double, double* %16, align 8
  %18 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 %indvars.iv3, i64 0
  %19 = load double, double* %18, align 8
  %20 = fmul double %17, %19
  %21 = fadd double %tmp.1, %20
  %indvars.iv.next4 = add nuw nsw i64 %indvars.iv3, 1
  br label %.preheader2

22:                                               ; preds = %.preheader2
  %23 = icmp eq i32 %n, 3
  br i1 %23, label %.preheader, label %.thread

.preheader:                                       ; preds = %24, %22
  %indvars.iv = phi i64 [ %indvars.iv.next, %24 ], [ 1, %22 ]
  %tmp.3 = phi double [ %31, %24 ], [ %tmp.1, %22 ]
  %exitcond = icmp eq i64 %indvars.iv, 4
  br i1 %exitcond, label %.thread, label %24

24:                                               ; preds = %.preheader
  %25 = add nsw i64 %indvars.iv, -1
  %26 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %25
  %27 = load double, double* %26, align 8
  %28 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 %indvars.iv, i64 0, i64 0
  %29 = load double, double* %28, align 8
  %30 = fmul double %27, %29
  %31 = fadd double %tmp.3, %30
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  br label %.preheader

.thread:                                          ; preds = %.preheader, %22, %12
  %tmp.4 = phi double [ %tmp.1, %22 ], [ %tmp.0, %12 ], [ %tmp.3, %.preheader ]
  store double %tmp.4, double* %tmor, align 8
  ret void
}

; Function Attrs: nounwind uwtable
define void @transfb_cor_f(i32 %n, double* nocapture %tmor, [5 x [5 x double]]* nocapture readonly %tx) local_unnamed_addr #0 {
  %temp = alloca [5 x double], align 16
  %1 = getelementptr inbounds [5 x double], [5 x double]* %temp, i64 0, i64 0
  call void @r_init(double* nonnull %1, i32 5, double 0.000000e+00) #3
  br label %2

2:                                                ; preds = %19, %0
  %indvars.iv35 = phi i64 [ %indvars.iv.next36, %19 ], [ 0, %0 ]
  %exitcond37 = icmp eq i64 %indvars.iv35, 5
  br i1 %exitcond37, label %20, label %3

3:                                                ; preds = %2
  %4 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 0, i64 %indvars.iv35
  %5 = bitcast double* %4 to i64*
  %6 = load i64, i64* %5, align 8
  %7 = getelementptr inbounds [5 x double], [5 x double]* %temp, i64 0, i64 %indvars.iv35
  %8 = bitcast double* %7 to i64*
  store i64 %6, i64* %8, align 8
  %.promoted7.cast = bitcast i64 %6 to double
  br label %9

9:                                                ; preds = %11, %3
  %indvars.iv32 = phi i64 [ %indvars.iv.next33, %11 ], [ 1, %3 ]
  %10 = phi double [ %18, %11 ], [ %.promoted7.cast, %3 ]
  %exitcond34 = icmp eq i64 %indvars.iv32, 4
  br i1 %exitcond34, label %19, label %11

11:                                               ; preds = %9
  %12 = add nsw i64 %indvars.iv32, -1
  %13 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %12
  %14 = load double, double* %13, align 8
  %15 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 0, i64 %indvars.iv32, i64 %indvars.iv35
  %16 = load double, double* %15, align 8
  %17 = fmul double %14, %16
  %18 = fadd double %10, %17
  %indvars.iv.next33 = add nuw nsw i64 %indvars.iv32, 1
  br label %9

19:                                               ; preds = %9
  store double %10, double* %7, align 8
  %indvars.iv.next36 = add nuw nsw i64 %indvars.iv35, 1
  br label %2

20:                                               ; preds = %2
  %21 = load double, double* %1, align 16
  br label %22

22:                                               ; preds = %23, %20
  %indvars.iv29 = phi i64 [ %indvars.iv.next30, %23 ], [ 1, %20 ]
  %tmp.0 = phi double [ %30, %23 ], [ %21, %20 ]
  %exitcond31 = icmp eq i64 %indvars.iv29, 4
  br i1 %exitcond31, label %31, label %23

23:                                               ; preds = %22
  %24 = add nsw i64 %indvars.iv29, -1
  %25 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %24
  %26 = load double, double* %25, align 8
  %27 = getelementptr inbounds [5 x double], [5 x double]* %temp, i64 0, i64 %indvars.iv29
  %28 = load double, double* %27, align 8
  %29 = fmul double %26, %28
  %30 = fadd double %tmp.0, %29
  %indvars.iv.next30 = add nuw nsw i64 %indvars.iv29, 1
  br label %22

31:                                               ; preds = %22
  %32 = icmp eq i32 %n, 5
  br i1 %32, label %.preheader4, label %.loopexit

.preheader4:                                      ; preds = %33, %31
  %indvars.iv26 = phi i64 [ %indvars.iv.next27, %33 ], [ 1, %31 ]
  %tmp.1 = phi double [ %40, %33 ], [ %tmp.0, %31 ]
  %exitcond28 = icmp eq i64 %indvars.iv26, 4
  br i1 %exitcond28, label %.loopexit, label %33

33:                                               ; preds = %.preheader4
  %34 = add nsw i64 %indvars.iv26, -1
  %35 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %34
  %36 = load double, double* %35, align 8
  %37 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 %indvars.iv26, i64 0, i64 0
  %38 = load double, double* %37, align 8
  %39 = fmul double %36, %38
  %40 = fadd double %tmp.1, %39
  %indvars.iv.next27 = add nuw nsw i64 %indvars.iv26, 1
  br label %.preheader4

.loopexit:                                        ; preds = %.preheader4, %31
  %tmp.2 = phi double [ %tmp.0, %31 ], [ %tmp.1, %.preheader4 ]
  %41 = icmp sgt i32 %n, 5
  br i1 %41, label %42, label %.thread

42:                                               ; preds = %.loopexit
  call void @r_init(double* nonnull %1, i32 5, double 0.000000e+00) #3
  br label %43

43:                                               ; preds = %55, %42
  %indvars.iv23 = phi i64 [ %indvars.iv.next24, %55 ], [ 0, %42 ]
  %exitcond25 = icmp eq i64 %indvars.iv23, 5
  br i1 %exitcond25, label %56, label %.preheader3

.preheader3:                                      ; preds = %43
  %44 = getelementptr inbounds [5 x double], [5 x double]* %temp, i64 0, i64 %indvars.iv23
  %.promoted5 = load double, double* %44, align 8
  br label %45

45:                                               ; preds = %47, %.preheader3
  %indvars.iv20 = phi i64 [ 1, %.preheader3 ], [ %indvars.iv.next21, %47 ]
  %46 = phi double [ %.promoted5, %.preheader3 ], [ %54, %47 ]
  %exitcond22 = icmp eq i64 %indvars.iv20, 4
  br i1 %exitcond22, label %55, label %47

47:                                               ; preds = %45
  %48 = add nsw i64 %indvars.iv20, -1
  %49 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %48
  %50 = load double, double* %49, align 8
  %51 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 %indvars.iv20, i64 0, i64 %indvars.iv23
  %52 = load double, double* %51, align 8
  %53 = fmul double %50, %52
  %54 = fadd double %46, %53
  %indvars.iv.next21 = add nuw nsw i64 %indvars.iv20, 1
  br label %45

55:                                               ; preds = %45
  store double %46, double* %44, align 8
  %indvars.iv.next24 = add nuw nsw i64 %indvars.iv23, 1
  br label %43

56:                                               ; preds = %43
  %57 = load double, double* %1, align 16
  %58 = fadd double %tmp.2, %57
  br label %59

59:                                               ; preds = %60, %56
  %indvars.iv17 = phi i64 [ %indvars.iv.next18, %60 ], [ 1, %56 ]
  %tmp.3 = phi double [ %67, %60 ], [ %58, %56 ]
  %exitcond19 = icmp eq i64 %indvars.iv17, 4
  br i1 %exitcond19, label %68, label %60

60:                                               ; preds = %59
  %61 = add nsw i64 %indvars.iv17, -1
  %62 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %61
  %63 = load double, double* %62, align 8
  %64 = getelementptr inbounds [5 x double], [5 x double]* %temp, i64 0, i64 %indvars.iv17
  %65 = load double, double* %64, align 8
  %66 = fmul double %63, %65
  %67 = fadd double %tmp.3, %66
  %indvars.iv.next18 = add nuw nsw i64 %indvars.iv17, 1
  br label %59

68:                                               ; preds = %59
  %69 = icmp eq i32 %n, 7
  br i1 %69, label %70, label %.thread

70:                                               ; preds = %68
  call void @r_init(double* nonnull %1, i32 5, double 0.000000e+00) #3
  br label %71

71:                                               ; preds = %83, %70
  %indvars.iv14 = phi i64 [ %indvars.iv.next15, %83 ], [ 1, %70 ]
  %exitcond16 = icmp eq i64 %indvars.iv14, 4
  br i1 %exitcond16, label %.preheader, label %.preheader2

.preheader2:                                      ; preds = %71
  %72 = getelementptr inbounds [5 x double], [5 x double]* %temp, i64 0, i64 %indvars.iv14
  %.promoted = load double, double* %72, align 8
  br label %73

73:                                               ; preds = %75, %.preheader2
  %indvars.iv11 = phi i64 [ 1, %.preheader2 ], [ %indvars.iv.next12, %75 ]
  %74 = phi double [ %.promoted, %.preheader2 ], [ %82, %75 ]
  %exitcond13 = icmp eq i64 %indvars.iv11, 4
  br i1 %exitcond13, label %83, label %75

75:                                               ; preds = %73
  %76 = add nsw i64 %indvars.iv11, -1
  %77 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %76
  %78 = load double, double* %77, align 8
  %79 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tx, i64 %indvars.iv11, i64 %indvars.iv14, i64 0
  %80 = load double, double* %79, align 8
  %81 = fmul double %78, %80
  %82 = fadd double %74, %81
  %indvars.iv.next12 = add nuw nsw i64 %indvars.iv11, 1
  br label %73

83:                                               ; preds = %73
  store double %74, double* %72, align 8
  %indvars.iv.next15 = add nuw nsw i64 %indvars.iv14, 1
  br label %71

.preheader:                                       ; preds = %84, %71
  %indvars.iv = phi i64 [ %indvars.iv.next, %84 ], [ 1, %71 ]
  %tmp.5 = phi double [ %91, %84 ], [ %tmp.3, %71 ]
  %exitcond = icmp eq i64 %indvars.iv, 4
  br i1 %exitcond, label %.thread, label %84

84:                                               ; preds = %.preheader
  %85 = add nsw i64 %indvars.iv, -1
  %86 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %85
  %87 = load double, double* %86, align 8
  %88 = getelementptr inbounds [5 x double], [5 x double]* %temp, i64 0, i64 %indvars.iv
  %89 = load double, double* %88, align 8
  %90 = fmul double %87, %89
  %91 = fadd double %tmp.5, %90
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  br label %.preheader

.thread:                                          ; preds = %.preheader, %68, %.loopexit
  %tmp.6 = phi double [ %tmp.3, %68 ], [ %tmp.2, %.loopexit ], [ %tmp.5, %.preheader ]
  store double %tmp.6, double* %tmor, align 8
  ret void
}

; Function Attrs: nounwind uwtable
define void @transf_nc([5 x double]* nocapture readonly %tmor, [5 x double]* nocapture %tx) local_unnamed_addr #0 {
  %tmp = alloca [5 x [5 x double]], align 16
  %1 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 0, i64 0
  call void @r_init(double* nonnull %1, i32 25, double 0.000000e+00) #3
  br label %2

2:                                                ; preds = %22, %0
  %indvars.iv15 = phi i64 [ %indvars.iv.next16, %22 ], [ 0, %0 ]
  %exitcond17 = icmp eq i64 %indvars.iv15, 5
  br i1 %exitcond17, label %.preheader1, label %3

3:                                                ; preds = %2
  %4 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv15, i64 0
  %5 = bitcast double* %4 to i64*
  %6 = load i64, i64* %5, align 8
  %7 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 %indvars.iv15
  %8 = bitcast [5 x double]* %7 to i64*
  store i64 %6, i64* %8, align 8
  br label %9

9:                                                ; preds = %21, %3
  %indvars.iv12 = phi i64 [ %indvars.iv.next13, %21 ], [ 1, %3 ]
  %exitcond14 = icmp eq i64 %indvars.iv12, 4
  br i1 %exitcond14, label %22, label %.preheader2

.preheader2:                                      ; preds = %9
  %10 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 %indvars.iv15, i64 %indvars.iv12
  %11 = add nsw i64 %indvars.iv12, -1
  %.promoted = load double, double* %10, align 8
  br label %12

12:                                               ; preds = %14, %.preheader2
  %indvars.iv9 = phi i64 [ 0, %.preheader2 ], [ %indvars.iv.next10, %14 ]
  %13 = phi double [ %.promoted, %.preheader2 ], [ %20, %14 ]
  %exitcond11 = icmp eq i64 %indvars.iv9, 5
  br i1 %exitcond11, label %21, label %14

14:                                               ; preds = %12
  %15 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv9, i64 %11
  %16 = load double, double* %15, align 8
  %17 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv15, i64 %indvars.iv9
  %18 = load double, double* %17, align 8
  %19 = fmul double %16, %18
  %20 = fadd double %13, %19
  %indvars.iv.next10 = add nuw nsw i64 %indvars.iv9, 1
  br label %12

21:                                               ; preds = %12
  store double %13, double* %10, align 8
  %indvars.iv.next13 = add nuw nsw i64 %indvars.iv12, 1
  br label %9

22:                                               ; preds = %9
  %indvars.iv.next16 = add nuw nsw i64 %indvars.iv15, 1
  br label %2

.preheader1:                                      ; preds = %42, %2
  %indvars.iv6 = phi i64 [ %indvars.iv.next7, %42 ], [ 0, %2 ]
  %exitcond8 = icmp eq i64 %indvars.iv6, 5
  br i1 %exitcond8, label %43, label %23

23:                                               ; preds = %.preheader1
  %24 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 0, i64 %indvars.iv6
  %25 = load double, double* %24, align 8
  %26 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 0, i64 %indvars.iv6
  %27 = load double, double* %26, align 8
  %28 = fadd double %25, %27
  store double %28, double* %24, align 8
  br label %29

29:                                               ; preds = %41, %23
  %indvars.iv3 = phi i64 [ %indvars.iv.next4, %41 ], [ 1, %23 ]
  %exitcond5 = icmp eq i64 %indvars.iv3, 4
  br i1 %exitcond5, label %42, label %.preheader

.preheader:                                       ; preds = %29
  %30 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 %indvars.iv3, i64 %indvars.iv6
  %31 = add nsw i64 %indvars.iv3, -1
  br label %32

32:                                               ; preds = %33, %.preheader
  %indvars.iv = phi i64 [ 0, %.preheader ], [ %indvars.iv.next, %33 ]
  %exitcond = icmp eq i64 %indvars.iv, 5
  br i1 %exitcond, label %41, label %33

33:                                               ; preds = %32
  %34 = load double, double* %30, align 8
  %35 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv, i64 %31
  %36 = load double, double* %35, align 8
  %37 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %tmp, i64 0, i64 %indvars.iv, i64 %indvars.iv6
  %38 = load double, double* %37, align 8
  %39 = fmul double %36, %38
  %40 = fadd double %34, %39
  store double %40, double* %30, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  br label %32

41:                                               ; preds = %32
  %indvars.iv.next4 = add nuw nsw i64 %indvars.iv3, 1
  br label %29

42:                                               ; preds = %29
  %indvars.iv.next7 = add nuw nsw i64 %indvars.iv6, 1
  br label %.preheader1

43:                                               ; preds = %.preheader1
  ret void
}

; Function Attrs: nounwind uwtable
define void @transfb_nc0([5 x double]* %tmor, [5 x [5 x double]]* nocapture readonly %tx) local_unnamed_addr #0 {
  %1 = getelementptr [5 x double], [5 x double]* %tmor, i64 0, i64 0
  tail call void @r_init(double* %1, i32 25, double 0.000000e+00) #3
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
  br label %4

14:                                               ; preds = %4
  %indvars.iv.next2 = add nuw nsw i64 %indvars.iv1, 1
  br label %2

15:                                               ; preds = %2
  ret void
}

; Function Attrs: nounwind uwtable
define void @transfb_nc2([5 x double]* %tmor, [5 x double]* nocapture readonly %tx) local_unnamed_addr #0 {
  %bottom = alloca [5 x double], align 16
  %temp = alloca [5 x [5 x double]], align 16
  %1 = getelementptr [5 x double], [5 x double]* %tmor, i64 0, i64 0
  tail call void @r_init(double* %1, i32 25, double 0.000000e+00) #3
  %2 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 0
  call void @r_init(double* nonnull %2, i32 25, double 0.000000e+00) #3
  %3 = bitcast [5 x double]* %tx to i64*
  %4 = load i64, i64* %3, align 8
  %5 = bitcast [5 x double]* %tmor to i64*
  store i64 %4, i64* %5, align 8
  br label %6

6:                                                ; preds = %37, %0
  %indvars.iv30 = phi i64 [ %indvars.iv.next31, %37 ], [ 0, %0 ]
  %exitcond32 = icmp eq i64 %indvars.iv30, 5
  br i1 %exitcond32, label %.preheader3, label %7

7:                                                ; preds = %6
  %8 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 0, i64 %indvars.iv30
  %9 = bitcast double* %8 to i64*
  %10 = load i64, i64* %9, align 8
  %11 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 %indvars.iv30
  %12 = bitcast double* %11 to i64*
  store i64 %10, i64* %12, align 8
  %13 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 %indvars.iv30
  store double 0.000000e+00, double* %13, align 8
  br label %14

14:                                               ; preds = %16, %7
  %indvars.iv21 = phi i64 [ %indvars.iv.next22, %16 ], [ 1, %7 ]
  %15 = phi double [ %23, %16 ], [ 0.000000e+00, %7 ]
  %exitcond23 = icmp eq i64 %indvars.iv21, 4
  br i1 %exitcond23, label %.preheader5, label %16

.preheader5:                                      ; preds = %14
  store double %15, double* %13, align 8
  br label %24

16:                                               ; preds = %14
  %17 = add nsw i64 %indvars.iv21, -1
  %18 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %17
  %19 = load double, double* %18, align 8
  %20 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 %indvars.iv21, i64 %indvars.iv30
  %21 = load double, double* %20, align 8
  %22 = fmul double %19, %21
  %23 = fadd double %15, %22
  %indvars.iv.next22 = add nuw nsw i64 %indvars.iv21, 1
  br label %14

24:                                               ; preds = %36, %.preheader5
  %indvars.iv27 = phi i64 [ 1, %.preheader5 ], [ %indvars.iv.next28, %36 ]
  %exitcond29 = icmp eq i64 %indvars.iv27, 5
  br i1 %exitcond29, label %37, label %.preheader4

.preheader4:                                      ; preds = %24
  %25 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv27, i64 %indvars.iv30
  %.promoted6 = load double, double* %25, align 8
  br label %26

26:                                               ; preds = %28, %.preheader4
  %indvars.iv24 = phi i64 [ 1, %.preheader4 ], [ %indvars.iv.next25, %28 ]
  %27 = phi double [ %.promoted6, %.preheader4 ], [ %35, %28 ]
  %exitcond26 = icmp eq i64 %indvars.iv24, 4
  br i1 %exitcond26, label %36, label %28

28:                                               ; preds = %26
  %29 = add nsw i64 %indvars.iv24, -1
  %30 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv27, i64 %29
  %31 = load double, double* %30, align 8
  %32 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 %indvars.iv24, i64 %indvars.iv30
  %33 = load double, double* %32, align 8
  %34 = fmul double %31, %33
  %35 = fadd double %27, %34
  %indvars.iv.next25 = add nuw nsw i64 %indvars.iv24, 1
  br label %26

36:                                               ; preds = %26
  store double %27, double* %25, align 8
  %indvars.iv.next28 = add nuw nsw i64 %indvars.iv27, 1
  br label %24

37:                                               ; preds = %24
  %indvars.iv.next31 = add nuw nsw i64 %indvars.iv30, 1
  br label %6

.preheader3:                                      ; preds = %54, %6
  %indvars.iv18 = phi i64 [ %indvars.iv.next19, %54 ], [ 0, %6 ]
  %exitcond20 = icmp eq i64 %indvars.iv18, 5
  br i1 %exitcond20, label %.preheader1, label %.preheader2

.preheader2:                                      ; preds = %.preheader3
  %38 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 %indvars.iv18
  br label %39

39:                                               ; preds = %40, %.preheader2
  %indvars.iv15 = phi i64 [ 1, %.preheader2 ], [ %indvars.iv.next16, %40 ]
  %exitcond17 = icmp eq i64 %indvars.iv15, 4
  br i1 %exitcond17, label %54, label %40

40:                                               ; preds = %39
  %41 = load double, double* %38, align 8
  %42 = add nsw i64 %indvars.iv15, -1
  %43 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv18, i64 %42
  %44 = load double, double* %43, align 8
  %45 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 %indvars.iv15
  %46 = load double, double* %45, align 8
  %47 = fmul double %44, %46
  %48 = fadd double %41, %47
  %49 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 %indvars.iv15
  %50 = load double, double* %49, align 8
  %51 = fmul double %44, %50
  %52 = fmul double %51, 5.000000e-01
  %53 = fadd double %48, %52
  store double %53, double* %38, align 8
  %indvars.iv.next16 = add nuw nsw i64 %indvars.iv15, 1
  br label %39

54:                                               ; preds = %39
  %indvars.iv.next19 = add nuw nsw i64 %indvars.iv18, 1
  br label %.preheader3

.preheader1:                                      ; preds = %74, %.preheader3
  %indvars.iv12 = phi i64 [ %indvars.iv.next13, %74 ], [ 1, %.preheader3 ]
  %exitcond14 = icmp eq i64 %indvars.iv12, 5
  br i1 %exitcond14, label %75, label %55

55:                                               ; preds = %.preheader1
  %56 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv12, i64 0
  %57 = load double, double* %56, align 8
  %58 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv12, i64 0
  %59 = load double, double* %58, align 8
  %60 = fadd double %57, %59
  store double %60, double* %56, align 8
  br label %61

61:                                               ; preds = %73, %55
  %indvars.iv9 = phi i64 [ %indvars.iv.next10, %73 ], [ 0, %55 ]
  %exitcond11 = icmp eq i64 %indvars.iv9, 5
  br i1 %exitcond11, label %74, label %.preheader

.preheader:                                       ; preds = %61
  %62 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv12, i64 %indvars.iv9
  br label %63

63:                                               ; preds = %64, %.preheader
  %indvars.iv = phi i64 [ 1, %.preheader ], [ %indvars.iv.next, %64 ]
  %exitcond = icmp eq i64 %indvars.iv, 4
  br i1 %exitcond, label %73, label %64

64:                                               ; preds = %63
  %65 = load double, double* %62, align 8
  %66 = add nsw i64 %indvars.iv, -1
  %67 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv9, i64 %66
  %68 = load double, double* %67, align 8
  %69 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv12, i64 %indvars.iv
  %70 = load double, double* %69, align 8
  %71 = fmul double %68, %70
  %72 = fadd double %65, %71
  store double %72, double* %62, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  br label %63

73:                                               ; preds = %63
  %indvars.iv.next10 = add nuw nsw i64 %indvars.iv9, 1
  br label %61

74:                                               ; preds = %61
  %indvars.iv.next13 = add nuw nsw i64 %indvars.iv12, 1
  br label %.preheader1

75:                                               ; preds = %.preheader1
  ret void
}

; Function Attrs: nounwind uwtable
define void @transfb_nc1([5 x double]* %tmor, [5 x double]* nocapture readonly %tx) local_unnamed_addr #0 {
  %bottom = alloca [5 x double], align 16
  %temp = alloca [5 x [5 x double]], align 16
  %1 = getelementptr [5 x double], [5 x double]* %tmor, i64 0, i64 0
  tail call void @r_init(double* %1, i32 25, double 0.000000e+00) #3
  %2 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 0
  call void @r_init(double* nonnull %2, i32 25, double 0.000000e+00) #3
  %3 = bitcast [5 x double]* %tx to i64*
  %4 = load i64, i64* %3, align 8
  %5 = bitcast [5 x double]* %tmor to i64*
  store i64 %4, i64* %5, align 8
  %6 = bitcast i64 %4 to double
  br label %7

7:                                                ; preds = %38, %0
  %indvars.iv29 = phi i64 [ %indvars.iv.next30, %38 ], [ 0, %0 ]
  %exitcond31 = icmp eq i64 %indvars.iv29, 5
  br i1 %exitcond31, label %39, label %8

8:                                                ; preds = %7
  %9 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 0, i64 %indvars.iv29
  %10 = bitcast double* %9 to i64*
  %11 = load i64, i64* %10, align 8
  %12 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 %indvars.iv29
  %13 = bitcast double* %12 to i64*
  store i64 %11, i64* %13, align 8
  %14 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 %indvars.iv29
  store double 0.000000e+00, double* %14, align 8
  br label %15

15:                                               ; preds = %17, %8
  %indvars.iv20 = phi i64 [ %indvars.iv.next21, %17 ], [ 1, %8 ]
  %16 = phi double [ %24, %17 ], [ 0.000000e+00, %8 ]
  %exitcond22 = icmp eq i64 %indvars.iv20, 4
  br i1 %exitcond22, label %.preheader4, label %17

.preheader4:                                      ; preds = %15
  store double %16, double* %14, align 8
  br label %25

17:                                               ; preds = %15
  %18 = add nsw i64 %indvars.iv20, -1
  %19 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 0, i64 %18
  %20 = load double, double* %19, align 8
  %21 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 %indvars.iv20, i64 %indvars.iv29
  %22 = load double, double* %21, align 8
  %23 = fmul double %20, %22
  %24 = fadd double %16, %23
  %indvars.iv.next21 = add nuw nsw i64 %indvars.iv20, 1
  br label %15

25:                                               ; preds = %37, %.preheader4
  %indvars.iv26 = phi i64 [ 1, %.preheader4 ], [ %indvars.iv.next27, %37 ]
  %exitcond28 = icmp eq i64 %indvars.iv26, 5
  br i1 %exitcond28, label %38, label %.preheader3

.preheader3:                                      ; preds = %25
  %26 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv26, i64 %indvars.iv29
  %.promoted5 = load double, double* %26, align 8
  br label %27

27:                                               ; preds = %29, %.preheader3
  %indvars.iv23 = phi i64 [ 1, %.preheader3 ], [ %indvars.iv.next24, %29 ]
  %28 = phi double [ %.promoted5, %.preheader3 ], [ %36, %29 ]
  %exitcond25 = icmp eq i64 %indvars.iv23, 4
  br i1 %exitcond25, label %37, label %29

29:                                               ; preds = %27
  %30 = add nsw i64 %indvars.iv23, -1
  %31 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv26, i64 %30
  %32 = load double, double* %31, align 8
  %33 = getelementptr inbounds [5 x double], [5 x double]* %tx, i64 %indvars.iv23, i64 %indvars.iv29
  %34 = load double, double* %33, align 8
  %35 = fmul double %32, %34
  %36 = fadd double %28, %35
  %indvars.iv.next24 = add nuw nsw i64 %indvars.iv23, 1
  br label %27

37:                                               ; preds = %27
  store double %28, double* %26, align 8
  %indvars.iv.next27 = add nuw nsw i64 %indvars.iv26, 1
  br label %25

38:                                               ; preds = %25
  %indvars.iv.next30 = add nuw nsw i64 %indvars.iv29, 1
  br label %7

39:                                               ; preds = %7
  %40 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 0
  %41 = load double, double* %40, align 16
  %42 = fadd double %41, %6
  store double %42, double* %1, align 8
  br label %43

43:                                               ; preds = %59, %39
  %indvars.iv17 = phi i64 [ %indvars.iv.next18, %59 ], [ 0, %39 ]
  %exitcond19 = icmp eq i64 %indvars.iv17, 5
  br i1 %exitcond19, label %.preheader1, label %.preheader2

.preheader2:                                      ; preds = %43
  %44 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 0, i64 %indvars.iv17
  br label %45

45:                                               ; preds = %46, %.preheader2
  %indvars.iv14 = phi i64 [ 1, %.preheader2 ], [ %indvars.iv.next15, %46 ]
  %exitcond16 = icmp eq i64 %indvars.iv14, 4
  br i1 %exitcond16, label %59, label %46

46:                                               ; preds = %45
  %47 = load double, double* %44, align 8
  %48 = add nsw i64 %indvars.iv14, -1
  %49 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv17, i64 %48
  %50 = load double, double* %49, align 8
  %51 = getelementptr inbounds [5 x double], [5 x double]* %bottom, i64 0, i64 %indvars.iv14
  %52 = load double, double* %51, align 8
  %53 = fmul double %50, %52
  %54 = fadd double %47, %53
  %55 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 0, i64 %indvars.iv14
  %56 = load double, double* %55, align 8
  %57 = fmul double %50, %56
  %58 = fadd double %54, %57
  store double %58, double* %44, align 8
  %indvars.iv.next15 = add nuw nsw i64 %indvars.iv14, 1
  br label %45

59:                                               ; preds = %45
  %indvars.iv.next18 = add nuw nsw i64 %indvars.iv17, 1
  br label %43

.preheader1:                                      ; preds = %79, %43
  %indvars.iv11 = phi i64 [ %indvars.iv.next12, %79 ], [ 1, %43 ]
  %exitcond13 = icmp eq i64 %indvars.iv11, 5
  br i1 %exitcond13, label %80, label %60

60:                                               ; preds = %.preheader1
  %61 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv11, i64 0
  %62 = load double, double* %61, align 8
  %63 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv11, i64 0
  %64 = load double, double* %63, align 8
  %65 = fadd double %62, %64
  store double %65, double* %61, align 8
  br label %66

66:                                               ; preds = %78, %60
  %indvars.iv8 = phi i64 [ %indvars.iv.next9, %78 ], [ 0, %60 ]
  %exitcond10 = icmp eq i64 %indvars.iv8, 5
  br i1 %exitcond10, label %79, label %.preheader

.preheader:                                       ; preds = %66
  %67 = getelementptr inbounds [5 x double], [5 x double]* %tmor, i64 %indvars.iv11, i64 %indvars.iv8
  br label %68

68:                                               ; preds = %69, %.preheader
  %indvars.iv = phi i64 [ 1, %.preheader ], [ %indvars.iv.next, %69 ]
  %exitcond = icmp eq i64 %indvars.iv, 4
  br i1 %exitcond, label %78, label %69

69:                                               ; preds = %68
  %70 = load double, double* %67, align 8
  %71 = add nsw i64 %indvars.iv, -1
  %72 = getelementptr inbounds [2 x [5 x [3 x double]]], [2 x [5 x [3 x double]]]* @qbnew, i64 0, i64 0, i64 %indvars.iv8, i64 %71
  %73 = load double, double* %72, align 8
  %74 = getelementptr inbounds [5 x [5 x double]], [5 x [5 x double]]* %temp, i64 0, i64 %indvars.iv11, i64 %indvars.iv
  %75 = load double, double* %74, align 8
  %76 = fmul double %73, %75
  %77 = fadd double %70, %76
  store double %77, double* %67, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  br label %68

78:                                               ; preds = %68
  %indvars.iv.next9 = add nuw nsw i64 %indvars.iv8, 1
  br label %66

79:                                               ; preds = %66
  %indvars.iv.next12 = add nuw nsw i64 %indvars.iv11, 1
  br label %.preheader1

80:                                               ; preds = %.preheader1
  ret void
}

; Function Attrs: nounwind uwtable
define void @transfb_c(double* nocapture readonly %tx) local_unnamed_addr #0 {
  %1 = load i32, i32* @nmor, align 4
  tail call void @r_init(double* getelementptr inbounds ([334600 x double], [334600 x double]* @tmort, i64 0, i64 0), i32 %1, double 0.000000e+00) #3
  %2 = load i32, i32* @nelt, align 4
  %3 = sext i32 %2 to i64
  br label %4

4:                                                ; preds = %138, %0
  %indvars.iv27 = phi i64 [ %indvars.iv.next28, %138 ], [ 0, %0 ]
  %5 = icmp slt i64 %indvars.iv27, %3
  br i1 %5, label %.preheader8, label %139

.preheader8:                                      ; preds = %.loopexit, %4
  %indvars.iv24 = phi i64 [ %indvars.iv.next25, %.loopexit ], [ 0, %4 ]
  %exitcond26 = icmp eq i64 %indvars.iv24, 6
  br i1 %exitcond26, label %138, label %6

6:                                                ; preds = %.preheader8
  %7 = getelementptr inbounds [8800 x [6 x i32]], [8800 x [6 x i32]]* @cbc, i64 0, i64 %indvars.iv27, i64 %indvars.iv24
  %8 = load i32, i32* %7, align 4
  %9 = icmp eq i32 %8, 3
  br i1 %9, label %.loopexit, label %10

10:                                               ; preds = %6
  %11 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0
  %12 = load i32, i32* %11, align 4
  %13 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 4
  %14 = load i32, i32* %13, align 4
  %15 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 4, i64 0
  %16 = load i32, i32* %15, align 4
  %17 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 4, i64 4
  %18 = load i32, i32* %17, align 4
  %19 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 0, i64 0
  %20 = load i32, i32* %19, align 16
  %21 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 1, i64 0, i64 0, i64 4
  %22 = load i32, i32* %21, align 8
  %23 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 1, i64 4, i64 0
  %24 = load i32, i32* %23, align 4
  %25 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 1, i64 1, i64 4, i64 4
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
  br label %59

59:                                               ; preds = %72, %10
  %indvars.iv9 = phi i64 [ %indvars.iv.next10, %72 ], [ 1, %10 ]
  %exitcond11 = icmp eq i64 %indvars.iv9, 4
  br i1 %exitcond11, label %73, label %.preheader

.preheader:                                       ; preds = %60, %59
  %indvars.iv = phi i64 [ %indvars.iv.next, %60 ], [ 1, %59 ]
  %exitcond = icmp eq i64 %indvars.iv, 4
  br i1 %exitcond, label %72, label %60

60:                                               ; preds = %.preheader
  %61 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 %indvars.iv9, i64 %indvars.iv
  %62 = load i32, i32* %61, align 4
  %63 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 %indvars.iv9, i64 %indvars.iv
  %64 = load i32, i32* %63, align 4
  %65 = sext i32 %64 to i64
  %66 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %65
  %67 = load double, double* %66, align 8
  %68 = sext i32 %62 to i64
  %69 = getelementptr inbounds double, double* %tx, i64 %68
  %70 = load double, double* %69, align 8
  %71 = fadd double %67, %70
  store double %71, double* %66, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  br label %.preheader

72:                                               ; preds = %.preheader
  %indvars.iv.next10 = add nuw nsw i64 %indvars.iv9, 1
  br label %59

73:                                               ; preds = %59
  %74 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 0, i64 4
  %75 = load i32, i32* %74, align 16
  %76 = icmp eq i32 %75, -1
  br i1 %76, label %.preheader6, label %.loopexit7

.preheader6:                                      ; preds = %77, %73
  %indvars.iv12 = phi i64 [ %indvars.iv.next13, %77 ], [ 1, %73 ]
  %exitcond14 = icmp eq i64 %indvars.iv12, 4
  br i1 %exitcond14, label %.loopexit7, label %77

77:                                               ; preds = %.preheader6
  %78 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 %indvars.iv12
  %79 = load i32, i32* %78, align 4
  %80 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 0, i64 %indvars.iv12
  %81 = load i32, i32* %80, align 4
  %82 = sext i32 %81 to i64
  %83 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %82
  %84 = load double, double* %83, align 8
  %85 = sext i32 %79 to i64
  %86 = getelementptr inbounds double, double* %tx, i64 %85
  %87 = load double, double* %86, align 8
  %88 = fmul double %87, 5.000000e-01
  %89 = fadd double %84, %88
  store double %89, double* %83, align 8
  %indvars.iv.next13 = add nuw nsw i64 %indvars.iv12, 1
  br label %.preheader6

.loopexit7:                                       ; preds = %.preheader6, %73
  %90 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 1, i64 0, i64 1, i64 4
  %91 = load i32, i32* %90, align 4
  %92 = icmp eq i32 %91, -1
  br i1 %92, label %.preheader4, label %.loopexit5

.preheader4:                                      ; preds = %93, %.loopexit7
  %indvars.iv15 = phi i64 [ %indvars.iv.next16, %93 ], [ 1, %.loopexit7 ]
  %exitcond17 = icmp eq i64 %indvars.iv15, 4
  br i1 %exitcond17, label %.loopexit5, label %93

93:                                               ; preds = %.preheader4
  %94 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 %indvars.iv15, i64 4
  %95 = load i32, i32* %94, align 4
  %96 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 %indvars.iv15, i64 4
  %97 = load i32, i32* %96, align 4
  %98 = sext i32 %97 to i64
  %99 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %98
  %100 = load double, double* %99, align 8
  %101 = sext i32 %95 to i64
  %102 = getelementptr inbounds double, double* %tx, i64 %101
  %103 = load double, double* %102, align 8
  %104 = fmul double %103, 5.000000e-01
  %105 = fadd double %100, %104
  store double %105, double* %99, align 8
  %indvars.iv.next16 = add nuw nsw i64 %indvars.iv15, 1
  br label %.preheader4

.loopexit5:                                       ; preds = %.preheader4, %.loopexit7
  %106 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 1, i64 4, i64 1
  %107 = load i32, i32* %106, align 4
  %108 = icmp eq i32 %107, -1
  br i1 %108, label %.preheader2, label %.loopexit3

.preheader2:                                      ; preds = %109, %.loopexit5
  %indvars.iv18 = phi i64 [ %indvars.iv.next19, %109 ], [ 1, %.loopexit5 ]
  %exitcond20 = icmp eq i64 %indvars.iv18, 4
  br i1 %exitcond20, label %.loopexit3, label %109

109:                                              ; preds = %.preheader2
  %110 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 4, i64 %indvars.iv18
  %111 = load i32, i32* %110, align 4
  %112 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 4, i64 %indvars.iv18
  %113 = load i32, i32* %112, align 4
  %114 = sext i32 %113 to i64
  %115 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %114
  %116 = load double, double* %115, align 8
  %117 = sext i32 %111 to i64
  %118 = getelementptr inbounds double, double* %tx, i64 %117
  %119 = load double, double* %118, align 8
  %120 = fmul double %119, 5.000000e-01
  %121 = fadd double %116, %120
  store double %121, double* %115, align 8
  %indvars.iv.next19 = add nuw nsw i64 %indvars.iv18, 1
  br label %.preheader2

.loopexit3:                                       ; preds = %.preheader2, %.loopexit5
  %122 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 4, i64 0
  %123 = load i32, i32* %122, align 16
  %124 = icmp eq i32 %123, -1
  br i1 %124, label %.preheader1, label %.loopexit

.preheader1:                                      ; preds = %125, %.loopexit3
  %indvars.iv21 = phi i64 [ %indvars.iv.next22, %125 ], [ 1, %.loopexit3 ]
  %exitcond23 = icmp eq i64 %indvars.iv21, 4
  br i1 %exitcond23, label %.loopexit, label %125

125:                                              ; preds = %.preheader1
  %126 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 %indvars.iv21, i64 0
  %127 = load i32, i32* %126, align 4
  %128 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 %indvars.iv21, i64 0
  %129 = load i32, i32* %128, align 4
  %130 = sext i32 %129 to i64
  %131 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %130
  %132 = load double, double* %131, align 8
  %133 = sext i32 %127 to i64
  %134 = getelementptr inbounds double, double* %tx, i64 %133
  %135 = load double, double* %134, align 8
  %136 = fmul double %135, 5.000000e-01
  %137 = fadd double %132, %136
  store double %137, double* %131, align 8
  %indvars.iv.next22 = add nuw nsw i64 %indvars.iv21, 1
  br label %.preheader1

.loopexit:                                        ; preds = %.preheader1, %.loopexit3, %6
  %indvars.iv.next25 = add nuw nsw i64 %indvars.iv24, 1
  br label %.preheader8

138:                                              ; preds = %.preheader8
  %indvars.iv.next28 = add nuw nsw i64 %indvars.iv27, 1
  br label %4

139:                                              ; preds = %4
  ret void
}

; Function Attrs: nounwind uwtable
define void @transfb_c_2(double* nocapture readonly %tx) local_unnamed_addr #0 {
  %1 = load i32, i32* @nmor, align 4
  tail call void @r_init(double* getelementptr inbounds ([334600 x double], [334600 x double]* @tmort, i64 0, i64 0), i32 %1, double 0.000000e+00) #3
  %2 = load i32, i32* @nmor, align 4
  tail call void @r_init(double* getelementptr inbounds ([334600 x double], [334600 x double]* @mormult, i64 0, i64 0), i32 %2, double 0.000000e+00) #3
  %3 = load i32, i32* @nelt, align 4
  %4 = sext i32 %3 to i64
  br label %5

5:                                                ; preds = %166, %0
  %indvars.iv27 = phi i64 [ %indvars.iv.next28, %166 ], [ 0, %0 ]
  %6 = icmp slt i64 %indvars.iv27, %4
  br i1 %6, label %.preheader8, label %167

.preheader8:                                      ; preds = %.loopexit, %5
  %indvars.iv24 = phi i64 [ %indvars.iv.next25, %.loopexit ], [ 0, %5 ]
  %exitcond26 = icmp eq i64 %indvars.iv24, 6
  br i1 %exitcond26, label %166, label %7

7:                                                ; preds = %.preheader8
  %8 = getelementptr inbounds [8800 x [6 x i32]], [8800 x [6 x i32]]* @cbc, i64 0, i64 %indvars.iv27, i64 %indvars.iv24
  %9 = load i32, i32* %8, align 4
  %10 = icmp eq i32 %9, 3
  br i1 %10, label %.loopexit, label %11

11:                                               ; preds = %7
  %12 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0
  %13 = load i32, i32* %12, align 4
  %14 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 4
  %15 = load i32, i32* %14, align 4
  %16 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 4, i64 0
  %17 = load i32, i32* %16, align 4
  %18 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 4, i64 4
  %19 = load i32, i32* %18, align 4
  %20 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 0, i64 0
  %21 = load i32, i32* %20, align 16
  %22 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 1, i64 0, i64 0, i64 4
  %23 = load i32, i32* %22, align 8
  %24 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 1, i64 4, i64 0
  %25 = load i32, i32* %24, align 4
  %26 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 1, i64 1, i64 4, i64 4
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
  br label %72

72:                                               ; preds = %88, %11
  %indvars.iv9 = phi i64 [ %indvars.iv.next10, %88 ], [ 1, %11 ]
  %exitcond11 = icmp eq i64 %indvars.iv9, 4
  br i1 %exitcond11, label %89, label %.preheader

.preheader:                                       ; preds = %73, %72
  %indvars.iv = phi i64 [ %indvars.iv.next, %73 ], [ 1, %72 ]
  %exitcond = icmp eq i64 %indvars.iv, 4
  br i1 %exitcond, label %88, label %73

73:                                               ; preds = %.preheader
  %74 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 %indvars.iv9, i64 %indvars.iv
  %75 = load i32, i32* %74, align 4
  %76 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 %indvars.iv9, i64 %indvars.iv
  %77 = load i32, i32* %76, align 4
  %78 = sext i32 %77 to i64
  %79 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %78
  %80 = load double, double* %79, align 8
  %81 = sext i32 %75 to i64
  %82 = getelementptr inbounds double, double* %tx, i64 %81
  %83 = load double, double* %82, align 8
  %84 = fadd double %80, %83
  store double %84, double* %79, align 8
  %85 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %78
  %86 = load double, double* %85, align 8
  %87 = fadd double %86, 1.000000e+00
  store double %87, double* %85, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  br label %.preheader

88:                                               ; preds = %.preheader
  %indvars.iv.next10 = add nuw nsw i64 %indvars.iv9, 1
  br label %72

89:                                               ; preds = %72
  %90 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 0, i64 4
  %91 = load i32, i32* %90, align 16
  %92 = icmp eq i32 %91, -1
  br i1 %92, label %.preheader6, label %.loopexit7

.preheader6:                                      ; preds = %93, %89
  %indvars.iv12 = phi i64 [ %indvars.iv.next13, %93 ], [ 1, %89 ]
  %exitcond14 = icmp eq i64 %indvars.iv12, 4
  br i1 %exitcond14, label %.loopexit7, label %93

93:                                               ; preds = %.preheader6
  %94 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 %indvars.iv12
  %95 = load i32, i32* %94, align 4
  %96 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 0, i64 %indvars.iv12
  %97 = load i32, i32* %96, align 4
  %98 = sext i32 %97 to i64
  %99 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %98
  %100 = load double, double* %99, align 8
  %101 = sext i32 %95 to i64
  %102 = getelementptr inbounds double, double* %tx, i64 %101
  %103 = load double, double* %102, align 8
  %104 = fmul double %103, 5.000000e-01
  %105 = fadd double %100, %104
  store double %105, double* %99, align 8
  %106 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %98
  %107 = load double, double* %106, align 8
  %108 = fadd double %107, 5.000000e-01
  store double %108, double* %106, align 8
  %indvars.iv.next13 = add nuw nsw i64 %indvars.iv12, 1
  br label %.preheader6

.loopexit7:                                       ; preds = %.preheader6, %89
  %109 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 1, i64 0, i64 1, i64 4
  %110 = load i32, i32* %109, align 4
  %111 = icmp eq i32 %110, -1
  br i1 %111, label %.preheader4, label %.loopexit5

.preheader4:                                      ; preds = %112, %.loopexit7
  %indvars.iv15 = phi i64 [ %indvars.iv.next16, %112 ], [ 1, %.loopexit7 ]
  %exitcond17 = icmp eq i64 %indvars.iv15, 4
  br i1 %exitcond17, label %.loopexit5, label %112

112:                                              ; preds = %.preheader4
  %113 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 %indvars.iv15, i64 4
  %114 = load i32, i32* %113, align 4
  %115 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 %indvars.iv15, i64 4
  %116 = load i32, i32* %115, align 4
  %117 = sext i32 %116 to i64
  %118 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %117
  %119 = load double, double* %118, align 8
  %120 = sext i32 %114 to i64
  %121 = getelementptr inbounds double, double* %tx, i64 %120
  %122 = load double, double* %121, align 8
  %123 = fmul double %122, 5.000000e-01
  %124 = fadd double %119, %123
  store double %124, double* %118, align 8
  %125 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %117
  %126 = load double, double* %125, align 8
  %127 = fadd double %126, 5.000000e-01
  store double %127, double* %125, align 8
  %indvars.iv.next16 = add nuw nsw i64 %indvars.iv15, 1
  br label %.preheader4

.loopexit5:                                       ; preds = %.preheader4, %.loopexit7
  %128 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 1, i64 4, i64 1
  %129 = load i32, i32* %128, align 4
  %130 = icmp eq i32 %129, -1
  br i1 %130, label %.preheader2, label %.loopexit3

.preheader2:                                      ; preds = %131, %.loopexit5
  %indvars.iv18 = phi i64 [ %indvars.iv.next19, %131 ], [ 1, %.loopexit5 ]
  %exitcond20 = icmp eq i64 %indvars.iv18, 4
  br i1 %exitcond20, label %.loopexit3, label %131

131:                                              ; preds = %.preheader2
  %132 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 4, i64 %indvars.iv18
  %133 = load i32, i32* %132, align 4
  %134 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 4, i64 %indvars.iv18
  %135 = load i32, i32* %134, align 4
  %136 = sext i32 %135 to i64
  %137 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %136
  %138 = load double, double* %137, align 8
  %139 = sext i32 %133 to i64
  %140 = getelementptr inbounds double, double* %tx, i64 %139
  %141 = load double, double* %140, align 8
  %142 = fmul double %141, 5.000000e-01
  %143 = fadd double %138, %142
  store double %143, double* %137, align 8
  %144 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %136
  %145 = load double, double* %144, align 8
  %146 = fadd double %145, 5.000000e-01
  store double %146, double* %144, align 8
  %indvars.iv.next19 = add nuw nsw i64 %indvars.iv18, 1
  br label %.preheader2

.loopexit3:                                       ; preds = %.preheader2, %.loopexit5
  %147 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 4, i64 0
  %148 = load i32, i32* %147, align 16
  %149 = icmp eq i32 %148, -1
  br i1 %149, label %.preheader1, label %.loopexit

.preheader1:                                      ; preds = %150, %.loopexit3
  %indvars.iv21 = phi i64 [ %indvars.iv.next22, %150 ], [ 1, %.loopexit3 ]
  %exitcond23 = icmp eq i64 %indvars.iv21, 4
  br i1 %exitcond23, label %.loopexit, label %150

150:                                              ; preds = %.preheader1
  %151 = getelementptr inbounds [8800 x [6 x [5 x [5 x i32]]]], [8800 x [6 x [5 x [5 x i32]]]]* @idel, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 %indvars.iv21, i64 0
  %152 = load i32, i32* %151, align 4
  %153 = getelementptr inbounds [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]], [8800 x [6 x [2 x [2 x [5 x [5 x i32]]]]]]* @idmo, i64 0, i64 %indvars.iv27, i64 %indvars.iv24, i64 0, i64 0, i64 %indvars.iv21, i64 0
  %154 = load i32, i32* %153, align 4
  %155 = sext i32 %154 to i64
  %156 = getelementptr inbounds [334600 x double], [334600 x double]* @tmort, i64 0, i64 %155
  %157 = load double, double* %156, align 8
  %158 = sext i32 %152 to i64
  %159 = getelementptr inbounds double, double* %tx, i64 %158
  %160 = load double, double* %159, align 8
  %161 = fmul double %160, 5.000000e-01
  %162 = fadd double %157, %161
  store double %162, double* %156, align 8
  %163 = getelementptr inbounds [334600 x double], [334600 x double]* @mormult, i64 0, i64 %155
  %164 = load double, double* %163, align 8
  %165 = fadd double %164, 5.000000e-01
  store double %165, double* %163, align 8
  %indvars.iv.next22 = add nuw nsw i64 %indvars.iv21, 1
  br label %.preheader1

.loopexit:                                        ; preds = %.preheader1, %.loopexit3, %7
  %indvars.iv.next25 = add nuw nsw i64 %indvars.iv24, 1
  br label %.preheader8

166:                                              ; preds = %.preheader8
  %indvars.iv.next28 = add nuw nsw i64 %indvars.iv27, 1
  br label %5

167:                                              ; preds = %5
  ret void
}

attributes #0 = { nounwind uwtable "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nofree norecurse nounwind uwtable "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind }
