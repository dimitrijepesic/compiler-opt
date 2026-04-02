; ModuleID = '-'
source_filename = "-"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "riscv64-unknown-linux-gnu"

%struct._IO_FILE = type { i32, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, %struct._IO_marker*, %struct._IO_FILE*, i32, i32, i64, i16, i8, [1 x i8], i8*, i64, %struct._IO_codecvt*, %struct._IO_wide_data*, %struct._IO_FILE*, i8*, i64, i32, [20 x i8] }
%struct._IO_marker = type opaque
%struct._IO_codecvt = type opaque
%struct._IO_wide_data = type opaque

@crc_32_tab = internal global [256 x i64] [i64 0, i64 1996959894, i64 3993919788, i64 2567524794, i64 124634137, i64 1886057615, i64 3915621685, i64 2657392035, i64 249268274, i64 2044508324, i64 3772115230, i64 2547177864, i64 162941995, i64 2125561021, i64 3887607047, i64 2428444049, i64 498536548, i64 1789927666, i64 4089016648, i64 2227061214, i64 450548861, i64 1843258603, i64 4107580753, i64 2211677639, i64 325883990, i64 1684777152, i64 4251122042, i64 2321926636, i64 335633487, i64 1661365465, i64 4195302755, i64 2366115317, i64 997073096, i64 1281953886, i64 3579855332, i64 2724688242, i64 1006888145, i64 1258607687, i64 3524101629, i64 2768942443, i64 901097722, i64 1119000684, i64 3686517206, i64 2898065728, i64 853044451, i64 1172266101, i64 3705015759, i64 2882616665, i64 651767980, i64 1373503546, i64 3369554304, i64 3218104598, i64 565507253, i64 1454621731, i64 3485111705, i64 3099436303, i64 671266974, i64 1594198024, i64 3322730930, i64 2970347812, i64 795835527, i64 1483230225, i64 3244367275, i64 3060149565, i64 1994146192, i64 31158534, i64 2563907772, i64 4023717930, i64 1907459465, i64 112637215, i64 2680153253, i64 3904427059, i64 2013776290, i64 251722036, i64 2517215374, i64 3775830040, i64 2137656763, i64 141376813, i64 2439277719, i64 3865271297, i64 1802195444, i64 476864866, i64 2238001368, i64 4066508878, i64 1812370925, i64 453092731, i64 2181625025, i64 4111451223, i64 1706088902, i64 314042704, i64 2344532202, i64 4240017532, i64 1658658271, i64 366619977, i64 2362670323, i64 4224994405, i64 1303535960, i64 984961486, i64 2747007092, i64 3569037538, i64 1256170817, i64 1037604311, i64 2765210733, i64 3554079995, i64 1131014506, i64 879679996, i64 2909243462, i64 3663771856, i64 1141124467, i64 855842277, i64 2852801631, i64 3708648649, i64 1342533948, i64 654459306, i64 3188396048, i64 3373015174, i64 1466479909, i64 544179635, i64 3110523913, i64 3462522015, i64 1591671054, i64 702138776, i64 2966460450, i64 3352799412, i64 1504918807, i64 783551873, i64 3082640443, i64 3233442989, i64 3988292384, i64 2596254646, i64 62317068, i64 1957810842, i64 3939845945, i64 2647816111, i64 81470997, i64 1943803523, i64 3814918930, i64 2489596804, i64 225274430, i64 2053790376, i64 3826175755, i64 2466906013, i64 167816743, i64 2097651377, i64 4027552580, i64 2265490386, i64 503444072, i64 1762050814, i64 4150417245, i64 2154129355, i64 426522225, i64 1852507879, i64 4275313526, i64 2312317920, i64 282753626, i64 1742555852, i64 4189708143, i64 2394877945, i64 397917763, i64 1622183637, i64 3604390888, i64 2714866558, i64 953729732, i64 1340076626, i64 3518719985, i64 2797360999, i64 1068828381, i64 1219638859, i64 3624741850, i64 2936675148, i64 906185462, i64 1090812512, i64 3747672003, i64 2825379669, i64 829329135, i64 1181335161, i64 3412177804, i64 3160834842, i64 628085408, i64 1382605366, i64 3423369109, i64 3138078467, i64 570562233, i64 1426400815, i64 3317316542, i64 2998733608, i64 733239954, i64 1555261956, i64 3268935591, i64 3050360625, i64 752459403, i64 1541320221, i64 2607071920, i64 3965973030, i64 1969922972, i64 40735498, i64 2617837225, i64 3943577151, i64 1913087877, i64 83908371, i64 2512341634, i64 3803740692, i64 2075208622, i64 213261112, i64 2463272603, i64 3855990285, i64 2094854071, i64 198958881, i64 2262029012, i64 4057260610, i64 1759359992, i64 534414190, i64 2176718541, i64 4139329115, i64 1873836001, i64 414664567, i64 2282248934, i64 4279200368, i64 1711684554, i64 285281116, i64 2405801727, i64 4167216745, i64 1634467795, i64 376229701, i64 2685067896, i64 3608007406, i64 1308918612, i64 956543938, i64 2808555105, i64 3495958263, i64 1231636301, i64 1047427035, i64 2932959818, i64 3654703836, i64 1088359270, i64 936918000, i64 2847714899, i64 3736837829, i64 1202900863, i64 817233897, i64 3183342108, i64 3401237130, i64 1404277552, i64 615818150, i64 3134207493, i64 3453421203, i64 1423857449, i64 601450431, i64 3009837614, i64 3294710456, i64 1567103746, i64 711928724, i64 3020668471, i64 3272380065, i64 1510334235, i64 755167117], align 16
@.str = private unnamed_addr constant [2 x i8] c"r\00", align 1
@.str.1 = private unnamed_addr constant [15 x i8] c"%08lX %7ld %s\0A\00", align 1
@.str.2 = private unnamed_addr constant [15 x i8] c"_finfo_dataset\00", align 1
@.str.1.3 = private unnamed_addr constant [3 x i8] c"rt\00", align 1
@stderr = external dso_local global %struct._IO_FILE*, align 8
@.str.2.4 = private unnamed_addr constant [29 x i8] c"\0AError: Can't find dataset!\0A\00", align 1
@.str.3 = private unnamed_addr constant [4 x i8] c"%ld\00", align 1

; Function Attrs: nounwind uwtable
define dso_local i64 @updateCRC32(i8 zeroext %0, i64 %1) #0 {
  %3 = zext i8 %0 to i64
  %.masked = and i64 %1, 255
  %4 = xor i64 %.masked, %3
  %5 = getelementptr inbounds [256 x i64], [256 x i64]* @crc_32_tab, i64 0, i64 %4
  %6 = load i64, i64* %5, align 8, !tbaa !0
  %7 = lshr i64 %1, 8
  %8 = xor i64 %6, %7
  ret i64 %8
}

; Function Attrs: nounwind uwtable
define dso_local i32 @crc32file(i8* %0, i64* %1, i64* %2) #0 {
  store i64 0, i64* %2, align 8, !tbaa !0
  %4 = call %struct._IO_FILE* @fopen(i8* %0, i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str, i64 0, i64 0)) #5
  %5 = icmp eq %struct._IO_FILE* %4, null
  br i1 %5, label %6, label %7

6:                                                ; preds = %3
  call void @perror(i8* %0) #6
  br label %27

7:                                                ; preds = %3, %10
  %.01 = phi i64 [ %19, %10 ], [ 4294967295, %3 ]
  %8 = call i32 @getc(%struct._IO_FILE* nonnull %4) #5
  %9 = icmp eq i32 %8, -1
  br i1 %9, label %20, label %10

10:                                               ; preds = %7
  %11 = load i64, i64* %2, align 8, !tbaa !0
  %12 = add nsw i64 %11, 1
  store i64 %12, i64* %2, align 8, !tbaa !0
  %13 = zext i32 %8 to i64
  %14 = xor i64 %.01, %13
  %15 = and i64 %14, 255
  %16 = getelementptr inbounds [256 x i64], [256 x i64]* @crc_32_tab, i64 0, i64 %15
  %17 = load i64, i64* %16, align 8, !tbaa !0
  %18 = lshr i64 %.01, 8
  %19 = xor i64 %17, %18
  br label %7

20:                                               ; preds = %7
  %21 = call i32 @ferror(%struct._IO_FILE* nonnull %4) #5
  %22 = icmp eq i32 %21, 0
  br i1 %22, label %24, label %23

23:                                               ; preds = %20
  call void @perror(i8* %0) #6
  store i64 -1, i64* %2, align 8, !tbaa !0
  br label %24

24:                                               ; preds = %20, %23
  %25 = call i32 @fclose(%struct._IO_FILE* nonnull %4) #5
  %26 = xor i64 %.01, -1
  store i64 %26, i64* %1, align 8, !tbaa !0
  br label %27

27:                                               ; preds = %24, %6
  %.0 = phi i32 [ -1, %6 ], [ 0, %24 ]
  ret i32 %.0
}

; Function Attrs: argmemonly nounwind willreturn
declare void @llvm.lifetime.start.p0i8(i64 immarg, i8* nocapture) #1

declare dso_local %struct._IO_FILE* @fopen(i8*, i8*) #2

declare dso_local void @perror(i8*) #2

declare dso_local i32 @getc(%struct._IO_FILE*) #2

; Function Attrs: nounwind
declare dso_local i32 @ferror(%struct._IO_FILE*) #3

declare dso_local i32 @fclose(%struct._IO_FILE*) #2

; Function Attrs: argmemonly nounwind willreturn
declare void @llvm.lifetime.end.p0i8(i64 immarg, i8* nocapture) #1

; Function Attrs: nounwind uwtable
define dso_local i64 @crc32buf(i8* %0, i64 %1) #0 {
  br label %3

3:                                                ; preds = %5, %2
  %.02 = phi i64 [ 4294967295, %2 ], [ %12, %5 ]
  %.01 = phi i64 [ %1, %2 ], [ %13, %5 ]
  %.0 = phi i8* [ %0, %2 ], [ %14, %5 ]
  %4 = icmp eq i64 %.01, 0
  br i1 %4, label %15, label %5

5:                                                ; preds = %3
  %6 = load i8, i8* %.0, align 1, !tbaa !4
  %7 = zext i8 %6 to i64
  %.02.masked = and i64 %.02, 255
  %8 = xor i64 %.02.masked, %7
  %9 = getelementptr inbounds [256 x i64], [256 x i64]* @crc_32_tab, i64 0, i64 %8
  %10 = load i64, i64* %9, align 8, !tbaa !0
  %11 = lshr i64 %.02, 8
  %12 = xor i64 %10, %11
  %13 = add i64 %.01, -1
  %14 = getelementptr inbounds i8, i8* %.0, i64 1
  br label %3

15:                                               ; preds = %3
  %16 = xor i64 %.02, -1
  ret i64 %16
}

; Function Attrs: nounwind uwtable
define dso_local i32 @main1(i32 %0, i8** %1, i32 %2) #0 {
  %4 = alloca i64, align 8
  %5 = alloca i64, align 8
  %6 = bitcast i64* %4 to i8*
  call void @llvm.lifetime.start.p0i8(i64 8, i8* nonnull %6) #5
  %7 = bitcast i64* %5 to i8*
  call void @llvm.lifetime.start.p0i8(i64 8, i8* nonnull %7) #5
  br label %8

8:                                                ; preds = %22, %3
  %.02 = phi i32 [ 0, %3 ], [ %15, %22 ]
  %.01 = phi i8** [ %1, %3 ], [ %12, %22 ]
  %.0 = phi i32 [ %0, %3 ], [ %9, %22 ]
  %9 = add nsw i32 %.0, -1
  %10 = icmp sgt i32 %.0, 1
  br i1 %10, label %11, label %23

11:                                               ; preds = %8
  %12 = getelementptr inbounds i8*, i8** %.01, i64 1
  %13 = load i8*, i8** %12, align 8, !tbaa !5
  %14 = call i32 @crc32file(i8* %13, i64* nonnull %4, i64* nonnull %5)
  %15 = or i32 %.02, %14
  %16 = icmp eq i32 %2, 0
  br i1 %16, label %22, label %17

17:                                               ; preds = %11
  %18 = load i64, i64* %4, align 8, !tbaa !0
  %19 = load i64, i64* %5, align 8, !tbaa !0
  %20 = load i8*, i8** %12, align 8, !tbaa !5
  %21 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([15 x i8], [15 x i8]* @.str.1, i64 0, i64 0), i64 %18, i64 %19, i8* %20) #5
  br label %22

22:                                               ; preds = %11, %17
  br label %8

23:                                               ; preds = %8
  %24 = icmp ne i32 %.02, 0
  %25 = zext i1 %24 to i32
  call void @llvm.lifetime.end.p0i8(i64 8, i8* nonnull %7) #5
  call void @llvm.lifetime.end.p0i8(i64 8, i8* nonnull %6) #5
  ret i32 %25
}

declare dso_local i32 @printf(i8*, ...) #2

; Function Attrs: nounwind uwtable
define dso_local i32 @main(i32 %0, i8** %1) #0 {
  %3 = alloca i64, align 8
  %4 = bitcast i64* %3 to i8*
  call void @llvm.lifetime.start.p0i8(i64 8, i8* nonnull %4) #5
  %5 = call %struct._IO_FILE* @fopen(i8* getelementptr inbounds ([15 x i8], [15 x i8]* @.str.2, i64 0, i64 0), i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.1.3, i64 0, i64 0)) #5
  %6 = icmp eq %struct._IO_FILE* %5, null
  br i1 %6, label %7, label %10

7:                                                ; preds = %2
  %8 = load %struct._IO_FILE*, %struct._IO_FILE** @stderr, align 8, !tbaa !5
  %9 = call i64 @fwrite(i8* getelementptr inbounds ([29 x i8], [29 x i8]* @.str.2.4, i64 0, i64 0), i64 28, i64 1, %struct._IO_FILE* %8) #7
  br label %21

10:                                               ; preds = %2
  %11 = call i32 (%struct._IO_FILE*, i8*, ...) @__isoc99_fscanf(%struct._IO_FILE* nonnull %5, i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.3, i64 0, i64 0), i64* nonnull %3) #5
  %12 = call i32 @fclose(%struct._IO_FILE* nonnull %5) #5
  br label %13

13:                                               ; preds = %16, %10
  %.01 = phi i64 [ 0, %10 ], [ %17, %16 ]
  %14 = load i64, i64* %3, align 8, !tbaa !0
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
  call void @llvm.lifetime.end.p0i8(i64 8, i8* nonnull %4) #5
  ret i32 %.0
}

declare dso_local i32 @fprintf(%struct._IO_FILE*, i8*, ...) #2

declare dso_local i32 @__isoc99_fscanf(%struct._IO_FILE*, i8*, ...) #2

; Function Attrs: nofree nounwind
declare i64 @fwrite(i8* nocapture, i64, i64, %struct._IO_FILE* nocapture) #4

attributes #0 = { nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="none" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8"   "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { argmemonly nounwind willreturn }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="none" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8"   "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="none" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8"   "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { nofree nounwind }
attributes #5 = { nounwind }
attributes #6 = { cold nounwind }
attributes #7 = { cold }

!0 = !{!1, !1, i64 0}
!1 = !{!"long", !2, i64 0}
!2 = !{!"omnipotent char", !3, i64 0}
!3 = !{!"Simple C/C++ TBAA"}
!4 = !{!2, !2, i64 0}
!5 = !{!6, !6, i64 0}
!6 = !{!"any pointer", !2, i64 0}
