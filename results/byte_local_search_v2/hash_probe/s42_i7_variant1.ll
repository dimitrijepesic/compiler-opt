source_filename = "-"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%union.U0 = type { i8* }

@.str = private unnamed_addr constant [2 x i8] c"1\00", align 1
@g_11 = internal global i64 2445994675441619566, align 8
@.str.1 = private unnamed_addr constant [5 x i8] c"g_11\00", align 1
@g_18 = internal global [9 x i32] [i32 -1, i32 -1, i32 -1, i32 -1, i32 -1, i32 -1, i32 -1, i32 -1, i32 -1], align 16
@.str.2 = private unnamed_addr constant [8 x i8] c"g_18[i]\00", align 1
@.str.3 = private unnamed_addr constant [14 x i8] c"index = [%d]\0A\00", align 1
@g_20 = internal global i8 -91, align 1
@.str.4 = private unnamed_addr constant [5 x i8] c"g_20\00", align 1
@g_58 = internal global i16 13271, align 2
@.str.5 = private unnamed_addr constant [5 x i8] c"g_58\00", align 1
@g_89 = internal unnamed_addr constant [8 x [7 x i16]] [[7 x i16] [i16 -13159, i16 1, i16 -16212, i16 26043, i16 -1, i16 26043, i16 -16212], [7 x i16] [i16 6, i16 6, i16 -1, i16 -7, i16 -1, i16 10895, i16 1057], [7 x i16] [i16 -13159, i16 26043, i16 22709, i16 22709, i16 26043, i16 -13159, i16 -1], [7 x i16] [i16 1, i16 -1, i16 30330, i16 30910, i16 -1, i16 -1, i16 30910], [7 x i16] [i16 0, i16 -4, i16 0, i16 1, i16 -1, i16 7424, i16 -13159], [7 x i16] [i16 30330, i16 -1, i16 1057, i16 30330, i16 1057, i16 6, i16 -2933], [7 x i16] [i16 -29117, i16 22709, i16 0, i16 1, i16 1, i16 -13159, i16 1], [7 x i16] [i16 6, i16 10895, i16 10895, i16 6, i16 31434, i16 1, i16 30330]], align 16
@.str.6 = private unnamed_addr constant [11 x i8] c"g_89[i][j]\00", align 1
@.str.7 = private unnamed_addr constant [18 x i8] c"index = [%d][%d]\0A\00", align 1
@g_91 = internal global [8 x i16] [i16 2853, i16 2853, i16 2853, i16 2853, i16 2853, i16 2853, i16 2853, i16 2853], align 16
@.str.8 = private unnamed_addr constant [8 x i8] c"g_91[i]\00", align 1
@g_111 = internal global i8 -46, align 1
@.str.9 = private unnamed_addr constant [6 x i8] c"g_111\00", align 1
@g_119 = internal global [2 x [1 x [7 x i32]]] [[1 x [7 x i32]] [[7 x i32] [i32 -572397696, i32 -572397696, i32 2, i32 -572397696, i32 -572397696, i32 2, i32 -572397696]], [1 x [7 x i32]] [[7 x i32] [i32 -572397696, i32 1714454574, i32 1714454574, i32 -572397696, i32 1714454574, i32 1714454574, i32 -572397696]]], align 16
@.str.10 = private unnamed_addr constant [15 x i8] c"g_119[i][j][k]\00", align 1
@.str.11 = private unnamed_addr constant [22 x i8] c"index = [%d][%d][%d]\0A\00", align 1
@g_131 = internal unnamed_addr global [4 x i64] [i64 -1, i64 -1, i64 -1, i64 -1], align 16
@.str.12 = private unnamed_addr constant [9 x i8] c"g_131[i]\00", align 1
@g_140 = internal unnamed_addr global i16 -29041, align 2
@.str.13 = private unnamed_addr constant [6 x i8] c"g_140\00", align 1
@g_142 = internal global i32 -1795765954, align 4
@.str.14 = private unnamed_addr constant [6 x i8] c"g_142\00", align 1
@g_171 = internal global i32 -1, align 4
@.str.15 = private unnamed_addr constant [6 x i8] c"g_171\00", align 1
@g_172 = internal global i32 -356812309, align 4
@.str.16 = private unnamed_addr constant [6 x i8] c"g_172\00", align 1
@g_320 = internal global i8 -107, align 1
@.str.17 = private unnamed_addr constant [6 x i8] c"g_320\00", align 1
@g_368 = internal global i32 1311598548, align 4
@.str.18 = private unnamed_addr constant [6 x i8] c"g_368\00", align 1
@g_397 = internal unnamed_addr global i16 28393, align 2
@.str.19 = private unnamed_addr constant [6 x i8] c"g_397\00", align 1
@g_400 = internal global i8 21, align 1
@.str.20 = private unnamed_addr constant [6 x i8] c"g_400\00", align 1
@g_512 = internal global i32 3, align 4
@.str.21 = private unnamed_addr constant [6 x i8] c"g_512\00", align 1
@.str.22 = private unnamed_addr constant [6 x i8] c"g_543\00", align 1
@g_575 = internal global i64 -5213770106506113412, align 8
@.str.23 = private unnamed_addr constant [6 x i8] c"g_575\00", align 1
@crc32_context = internal unnamed_addr global i32 -1, align 4
@crc32_tab = internal unnamed_addr global [256 x i32] zeroinitializer, align 16
@g_118 = internal global i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 1, i64 0, i64 0), align 8
@g_215 = internal unnamed_addr global i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 8), align 8
@g_432 = internal global i16* @g_58, align 8
@__const.func_2.l_509 = private unnamed_addr constant [1 x [3 x [9 x i32]]] [[3 x [9 x i32]] [[9 x i32] [i32 9, i32 9, i32 9, i32 9, i32 9, i32 9, i32 9, i32 9, i32 9], [9 x i32] [i32 -1914901143, i32 -1914901143, i32 -1914901143, i32 -1914901143, i32 -1914901143, i32 -1914901143, i32 -1914901143, i32 -1914901143, i32 -1914901143], [9 x i32] [i32 9, i32 9, i32 9, i32 9, i32 9, i32 9, i32 9, i32 9, i32 9]]], align 16
@g_44 = internal global i8* @g_20, align 8
@g_543 = internal constant i8 -20, align 1
@g_427 = internal global i32* @g_171, align 8
@g_141 = internal global [6 x i32*] [i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*)], align 16
@g_635 = internal unnamed_addr global i8**** getelementptr inbounds ([5 x i8***], [5 x i8***]* @g_636, i64 0, i64 3), align 8
@g_636 = internal global [5 x i8***] [i8*** @g_637, i8*** @g_637, i8*** @g_637, i8*** @g_637, i8*** @g_637], align 16
@g_637 = internal global i8** getelementptr inbounds ([4 x [8 x [4 x i8*]]], [4 x [8 x [4 x i8*]]]* @g_638, i64 0, i64 3, i64 4, i64 0), align 8
@g_638 = internal global [4 x [8 x [4 x i8*]]] [[8 x [4 x i8*]] [[4 x i8*] [i8* @g_400, i8* @g_400, i8* null, i8* @g_400], [4 x i8*] [i8* @g_400, i8* @g_20, i8* @g_20, i8* @g_400], [4 x i8*] [i8* @g_20, i8* @g_320, i8* null, i8* @g_400], [4 x i8*] [i8* @g_20, i8* null, i8* @g_320, i8* @g_320], [4 x i8*] [i8* @g_20, i8* @g_400, i8* null, i8* @g_320], [4 x i8*] [i8* null, i8* null, i8* @g_20, i8* @g_400], [4 x i8*] [i8* @g_400, i8* @g_320, i8* @g_20, i8* @g_400], [4 x i8*] [i8* null, i8* @g_20, i8* @g_20, i8* @g_400]], [8 x [4 x i8*]] [[4 x i8*] [i8* null, i8* @g_400, i8* null, i8* @g_400], [4 x i8*] [i8* @g_20, i8* @g_20, i8* null, i8* null], [4 x i8*] [i8* @g_320, i8* @g_400, i8* null, i8* @g_400], [4 x i8*] [i8* @g_20, i8* @g_20, i8* @g_20, i8* @g_20], [4 x i8*] [i8* @g_320, i8* null, i8* @g_400, i8* null], [4 x i8*] [i8* null, i8* @g_20, i8* @g_20, i8* @g_400], [4 x i8*] [i8* null, i8* @g_400, i8* @g_400, i8* @g_400], [4 x i8*] [i8* @g_320, i8* @g_400, i8* @g_20, i8* @g_320]], [8 x [4 x i8*]] [[4 x i8*] [i8* @g_20, i8* @g_400, i8* null, i8* @g_320], [4 x i8*] [i8* @g_320, i8* @g_20, i8* null, i8* @g_20], [4 x i8*] [i8* @g_20, i8* @g_400, i8* null, i8* @g_400], [4 x i8*] [i8* null, i8* @g_20, i8* @g_20, i8* @g_20], [4 x i8*] [i8* null, i8* null, i8* @g_20, i8* @g_20], [4 x i8*] [i8* @g_400, i8* @g_320, i8* @g_20, i8* null], [4 x i8*] [i8* @g_320, i8* @g_400, i8* @g_20, i8* @g_20], [4 x i8*] [i8* @g_400, i8* @g_400, i8* null, i8* null]], [8 x [4 x i8*]] [[4 x i8*] [i8* @g_400, i8* @g_320, i8* @g_400, i8* @g_400], [4 x i8*] [i8* null, i8* null, i8* null, i8* @g_400], [4 x i8*] [i8* @g_20, i8* @g_20, i8* null, i8* @g_20], [4 x i8*] [i8* @g_400, i8* @g_400, i8* @g_20, i8* @g_400], [4 x i8*] [i8* null, i8* @g_20, i8* @g_320, i8* null], [4 x i8*] [i8* @g_20, i8* @g_20, i8* @g_20, i8* @g_20], [4 x i8*] [i8* @g_400, i8* @g_20, i8* @g_320, i8* @g_320], [4 x i8*] [i8* null, i8* @g_400, i8* null, i8* @g_20]]], align 16
@g_106 = internal global %union.U0 zeroinitializer, align 8
@__const.func_67.l_117 = private unnamed_addr constant [4 x [9 x [7 x i32]]] [[9 x [7 x i32]] [[7 x i32] [i32 -1854576997, i32 -10, i32 -132096905, i32 3, i32 -8, i32 0, i32 616214352], [7 x i32] [i32 644334297, i32 -1, i32 395129846, i32 3, i32 1, i32 1, i32 -6], [7 x i32] [i32 -666901769, i32 -1, i32 0, i32 598164268, i32 1, i32 1002172723, i32 0], [7 x i32] [i32 -4, i32 0, i32 -529762007, i32 1371323651, i32 0, i32 -6, i32 0], [7 x i32] [i32 0, i32 -1, i32 8, i32 -6, i32 -2084893204, i32 0, i32 0], [7 x i32] [i32 1, i32 -1898913509, i32 0, i32 395129846, i32 -1959817787, i32 7, i32 -1959817787], [7 x i32] [i32 -2020256058, i32 9, i32 9, i32 -2020256058, i32 1, i32 -4, i32 2094105380], [7 x i32] [i32 1738015974, i32 1, i32 -3, i32 644334297, i32 1368777155, i32 -1857300812, i32 0], [7 x i32] [i32 196414362, i32 5, i32 1046977674, i32 -50136740, i32 0, i32 -6, i32 2094105380]], [9 x [7 x i32]] [[7 x i32] [i32 -1898913509, i32 7, i32 -4, i32 1195450976, i32 -6, i32 1, i32 -1959817787], [7 x i32] [i32 616214352, i32 0, i32 0, i32 -10, i32 8, i32 0, i32 0], [7 x i32] [i32 -3, i32 -1857300812, i32 -1, i32 -1, i32 -1777700, i32 1, i32 0], [7 x i32] [i32 2094105380, i32 1061555381, i32 -595724751, i32 8, i32 1000399752, i32 -6, i32 0], [7 x i32] [i32 -101267165, i32 -6, i32 -1, i32 -9, i32 -9, i32 -1, i32 -6], [7 x i32] [i32 -8, i32 638244229, i32 -6, i32 0, i32 0, i32 -132096905, i32 616214352], [7 x i32] [i32 0, i32 644334297, i32 -8, i32 -1, i32 -764956739, i32 1371323651, i32 1], [7 x i32] [i32 692398238, i32 2094105380, i32 -1, i32 0, i32 196414362, i32 -8, i32 -132096905], [7 x i32] [i32 2, i32 1, i32 524824689, i32 -9, i32 -1, i32 -1776562575, i32 -10]], [9 x [7 x i32]] [[7 x i32] [i32 9, i32 -2110602377, i32 1061555381, i32 8, i32 2, i32 1, i32 1002172723], [7 x i32] [i32 0, i32 4, i32 0, i32 -1, i32 1368777155, i32 1, i32 2], [7 x i32] [i32 0, i32 -1, i32 73832907, i32 8, i32 5, i32 -2, i32 -2], [7 x i32] [i32 0, i32 0, i32 395129846, i32 0, i32 0, i32 -1, i32 4], [7 x i32] [i32 -1, i32 0, i32 -1, i32 1002172723, i32 -2020256058, i32 1, i32 -6], [7 x i32] [i32 -1898913509, i32 1356777430, i32 1, i32 1738015974, i32 730521578, i32 -5, i32 -764956739], [7 x i32] [i32 -1, i32 1002172723, i32 -4, i32 -2, i32 692398238, i32 0, i32 1], [7 x i32] [i32 0, i32 -8, i32 1, i32 4, i32 -3, i32 -1857300812, i32 -1], [7 x i32] [i32 0, i32 1917141367, i32 196414362, i32 1061555381, i32 1002172723, i32 3, i32 0]], [9 x [7 x i32]] [[7 x i32] [i32 -9, i32 644334297, i32 524824689, i32 -1959817787, i32 1, i32 1, i32 4], [7 x i32] [i32 3, i32 0, i32 2094105380, i32 0, i32 -666901769, i32 0, i32 2094105380], [7 x i32] [i32 1914679593, i32 1914679593, i32 -1777700, i32 -4, i32 0, i32 1, i32 1356777430], [7 x i32] [i32 -1, i32 -5, i32 9, i32 0, i32 196414362, i32 -1, i32 0], [7 x i32] [i32 -1857300812, i32 0, i32 3, i32 -1776562575, i32 0, i32 -1719010738, i32 1738015974], [7 x i32] [i32 1936539133, i32 -8, i32 0, i32 355777422, i32 -666901769, i32 1002172723, i32 -1572771637], [7 x i32] [i32 -448216751, i32 -4, i32 -8, i32 -1, i32 1, i32 -1, i32 -3], [7 x i32] [i32 -1854576997, i32 -2, i32 -2084893204, i32 0, i32 1002172723, i32 -1, i32 -1], [7 x i32] [i32 1, i32 7, i32 1195450976, i32 730521578, i32 -3, i32 524824689, i32 841778661]]], align 16
@g_211 = internal global [7 x [2 x i32*]] [[2 x i32*] [i32* @g_171, i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*)], [2 x i32*] [i32* null, i32* @g_142], [2 x i32*] [i32* @g_142, i32* null], [2 x i32*] [i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* @g_171], [2 x i32*] [i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* null], [2 x i32*] [i32* @g_142, i32* @g_142], [2 x i32*] [i32* null, i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*)]], align 16
@.str.24 = private unnamed_addr constant [36 x i8] c"...checksum after hashing %s : %lX\0A\00", align 1
@.str.25 = private unnamed_addr constant [15 x i8] c"checksum = %X\0A\00", align 1

; Function Attrs: minsize nounwind optsize uwtable
define dso_local i32 @main(i32 %0, i8** %1) local_unnamed_addr #0 {
  %3 = icmp eq i32 %0, 2
  br i1 %3, label %4, label %10

4:                                                ; preds = %2
  %5 = getelementptr inbounds i8*, i8** %1, i64 1
  %6 = load i8*, i8** %5, align 8, !tbaa !0
  %7 = call i32 @strcmp(i8* nonnull dereferenceable(1) %6, i8* nonnull dereferenceable(2) getelementptr inbounds ([2 x i8], [2 x i8]* @.str, i64 0, i64 0)) #4
  %8 = icmp eq i32 %7, 0
  br i1 %8, label %9, label %10

9:                                                ; preds = %4
  br label %10

10:                                               ; preds = %9, %4, %2
  %phiofops17 = phi i1 [ true, %2 ], [ true, %4 ], [ false, %9 ]
  %.0 = phi i32 [ 1, %9 ], [ 0, %4 ], [ 0, %2 ]
  call fastcc void @platform_main_begin()
  call fastcc void @crc32_gentab()
  %11 = call fastcc signext i16 @func_1()
  %12 = load i64, i64* @g_11, align 8, !tbaa !4
  call fastcc void @transparent_crc(i64 %12, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.1, i64 0, i64 0), i32 %.0)
  br label %13

13:                                               ; preds = %22, %10
  %storemerge = phi i32 [ 0, %10 ], [ %23, %22 ]
  %14 = icmp slt i32 %storemerge, 9
  br i1 %14, label %15, label %24

15:                                               ; preds = %13
  %16 = sext i32 %storemerge to i64
  %17 = getelementptr inbounds [9 x i32], [9 x i32]* @g_18, i64 0, i64 %16
  %18 = load i32, i32* %17, align 4, !tbaa !6
  %19 = sext i32 %18 to i64
  call fastcc void @transparent_crc(i64 %19, i8* getelementptr inbounds ([8 x i8], [8 x i8]* @.str.2, i64 0, i64 0), i32 %.0)
  br i1 %phiofops17, label %22, label %20

20:                                               ; preds = %15
  %21 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([14 x i8], [14 x i8]* @.str.3, i64 0, i64 0), i32 %storemerge) #5
  br label %22

22:                                               ; preds = %20, %15
  %23 = add nsw i32 %storemerge, 1
  br label %13

24:                                               ; preds = %13
  %25 = load i8, i8* @g_20, align 1, !tbaa !8
  %26 = sext i8 %25 to i64
  call fastcc void @transparent_crc(i64 %26, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.4, i64 0, i64 0), i32 %.0)
  %27 = load i16, i16* @g_58, align 2, !tbaa !9
  %28 = sext i16 %27 to i64
  call fastcc void @transparent_crc(i64 %28, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.5, i64 0, i64 0), i32 %.0)
  br label %29

29:                                               ; preds = %44, %24
  %storemerge6 = phi i32 [ 0, %24 ], [ %45, %44 ]
  %30 = icmp slt i32 %storemerge6, 8
  br i1 %30, label %31, label %46

31:                                               ; preds = %29
  br label %32

32:                                               ; preds = %42, %31
  %storemerge12 = phi i32 [ 0, %31 ], [ %43, %42 ]
  %33 = icmp ult i32 %storemerge12, 7
  br i1 %33, label %34, label %44

34:                                               ; preds = %32
  %35 = sext i32 %storemerge6 to i64
  %36 = zext i32 %storemerge12 to i64
  %37 = getelementptr inbounds [8 x [7 x i16]], [8 x [7 x i16]]* @g_89, i64 0, i64 %35, i64 %36
  %38 = load i16, i16* %37, align 2, !tbaa !9
  %39 = zext i16 %38 to i64
  call fastcc void @transparent_crc(i64 %39, i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.6, i64 0, i64 0), i32 %.0)
  br i1 %phiofops17, label %42, label %40

40:                                               ; preds = %34
  %41 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([18 x i8], [18 x i8]* @.str.7, i64 0, i64 0), i32 %storemerge6, i32 %storemerge12) #5
  br label %42

42:                                               ; preds = %40, %34
  %43 = add nuw nsw i32 %storemerge12, 1
  br label %32

44:                                               ; preds = %32
  %45 = add nsw i32 %storemerge6, 1
  br label %29

46:                                               ; preds = %29
  br label %47

47:                                               ; preds = %56, %46
  %storemerge7 = phi i32 [ 0, %46 ], [ %57, %56 ]
  %48 = icmp slt i32 %storemerge7, 8
  br i1 %48, label %49, label %58

49:                                               ; preds = %47
  %50 = sext i32 %storemerge7 to i64
  %51 = getelementptr inbounds [8 x i16], [8 x i16]* @g_91, i64 0, i64 %50
  %52 = load i16, i16* %51, align 2, !tbaa !9
  %53 = zext i16 %52 to i64
  call fastcc void @transparent_crc(i64 %53, i8* getelementptr inbounds ([8 x i8], [8 x i8]* @.str.8, i64 0, i64 0), i32 %.0)
  br i1 %phiofops17, label %56, label %54

54:                                               ; preds = %49
  %55 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([14 x i8], [14 x i8]* @.str.3, i64 0, i64 0), i32 %storemerge7) #5
  br label %56

56:                                               ; preds = %54, %49
  %57 = add nsw i32 %storemerge7, 1
  br label %47

58:                                               ; preds = %47
  %59 = load i8, i8* @g_111, align 1, !tbaa !8
  %60 = zext i8 %59 to i64
  call fastcc void @transparent_crc(i64 %60, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.9, i64 0, i64 0), i32 %.0)
  br label %61

61:                                               ; preds = %79, %58
  %storemerge8 = phi i32 [ 0, %58 ], [ %80, %79 ]
  %62 = icmp slt i32 %storemerge8, 2
  br i1 %62, label %63, label %81

63:                                               ; preds = %61
  br label %64

64:                                               ; preds = %78, %63
  %phiofops = phi i1 [ true, %63 ], [ false, %78 ]
  br i1 %phiofops, label %65, label %79

65:                                               ; preds = %64
  br label %66

66:                                               ; preds = %76, %65
  %storemerge11 = phi i32 [ 0, %65 ], [ %77, %76 ]
  %67 = icmp ult i32 %storemerge11, 7
  br i1 %67, label %68, label %78

68:                                               ; preds = %66
  %69 = sext i32 %storemerge8 to i64
  %70 = zext i32 %storemerge11 to i64
  %71 = getelementptr inbounds [2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 %69, i64 0, i64 %70
  %72 = load i32, i32* %71, align 4, !tbaa !6
  %73 = sext i32 %72 to i64
  call fastcc void @transparent_crc(i64 %73, i8* getelementptr inbounds ([15 x i8], [15 x i8]* @.str.10, i64 0, i64 0), i32 %.0)
  br i1 %phiofops17, label %76, label %74

74:                                               ; preds = %68
  %75 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([22 x i8], [22 x i8]* @.str.11, i64 0, i64 0), i32 %storemerge8, i32 0, i32 %storemerge11) #5
  br label %76

76:                                               ; preds = %74, %68
  %77 = add nuw nsw i32 %storemerge11, 1
  br label %66

78:                                               ; preds = %66
  br label %64

79:                                               ; preds = %64
  %80 = add nsw i32 %storemerge8, 1
  br label %61

81:                                               ; preds = %61
  br label %82

82:                                               ; preds = %90, %81
  %storemerge9 = phi i32 [ 0, %81 ], [ %91, %90 ]
  %83 = icmp slt i32 %storemerge9, 4
  br i1 %83, label %84, label %92

84:                                               ; preds = %82
  %85 = sext i32 %storemerge9 to i64
  %86 = getelementptr inbounds [4 x i64], [4 x i64]* @g_131, i64 0, i64 %85
  %87 = load i64, i64* %86, align 8, !tbaa !4
  call fastcc void @transparent_crc(i64 %87, i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.str.12, i64 0, i64 0), i32 %.0)
  br i1 %phiofops17, label %90, label %88

88:                                               ; preds = %84
  %89 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([14 x i8], [14 x i8]* @.str.3, i64 0, i64 0), i32 %storemerge9) #5
  br label %90

90:                                               ; preds = %88, %84
  %91 = add nsw i32 %storemerge9, 1
  br label %82

92:                                               ; preds = %82
  %93 = load i16, i16* @g_140, align 2, !tbaa !9
  %94 = sext i16 %93 to i64
  call fastcc void @transparent_crc(i64 %94, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.13, i64 0, i64 0), i32 %.0)
  %95 = load i32, i32* @g_142, align 4, !tbaa !6
  %96 = sext i32 %95 to i64
  call fastcc void @transparent_crc(i64 %96, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.14, i64 0, i64 0), i32 %.0)
  %97 = load i32, i32* @g_171, align 4, !tbaa !6
  %98 = sext i32 %97 to i64
  call fastcc void @transparent_crc(i64 %98, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.15, i64 0, i64 0), i32 %.0)
  %99 = load i32, i32* @g_172, align 4, !tbaa !6
  %100 = zext i32 %99 to i64
  call fastcc void @transparent_crc(i64 %100, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.16, i64 0, i64 0), i32 %.0)
  %101 = load i8, i8* @g_320, align 1, !tbaa !8
  %102 = sext i8 %101 to i64
  call fastcc void @transparent_crc(i64 %102, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.17, i64 0, i64 0), i32 %.0)
  %103 = load volatile i32, i32* @g_368, align 4, !tbaa !6
  %104 = sext i32 %103 to i64
  call fastcc void @transparent_crc(i64 %104, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.18, i64 0, i64 0), i32 %.0)
  %105 = load i16, i16* @g_397, align 2, !tbaa !9
  %106 = sext i16 %105 to i64
  call fastcc void @transparent_crc(i64 %106, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.19, i64 0, i64 0), i32 %.0)
  %107 = load i8, i8* @g_400, align 1, !tbaa !8
  %108 = sext i8 %107 to i64
  call fastcc void @transparent_crc(i64 %108, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.20, i64 0, i64 0), i32 %.0)
  %109 = load i32, i32* @g_512, align 4, !tbaa !6
  %110 = zext i32 %109 to i64
  call fastcc void @transparent_crc(i64 %110, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.21, i64 0, i64 0), i32 %.0)
  call fastcc void @transparent_crc(i64 236, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.22, i64 0, i64 0), i32 %.0)
  %111 = load i64, i64* @g_575, align 8, !tbaa !4
  call fastcc void @transparent_crc(i64 %111, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.23, i64 0, i64 0), i32 %.0)
  %112 = load i32, i32* @crc32_context, align 4, !tbaa !6
  %113 = xor i32 %112, -1
  call fastcc void @platform_main_end(i32 %113, i32 %.0)
  ret i32 0
}

; Function Attrs: argmemonly nounwind willreturn
declare void @llvm.lifetime.start.p0i8(i64 immarg, i8* nocapture) #1

; Function Attrs: nounwind readonly
declare dso_local i32 @strcmp(i8*, i8*) local_unnamed_addr #2

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc void @platform_main_begin() unnamed_addr #0 {
  ret void
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc void @crc32_gentab() unnamed_addr #0 {
  br label %1

1:                                                ; preds = %15, %0
  %storemerge = phi i32 [ 0, %0 ], [ %18, %15 ]
  %2 = icmp ult i32 %storemerge, 256
  br i1 %2, label %3, label %19

3:                                                ; preds = %1
  br label %4

4:                                                ; preds = %13, %3
  %.0 = phi i32 [ %storemerge, %3 ], [ %storemerge3, %13 ]
  %storemerge2 = phi i32 [ 8, %3 ], [ %14, %13 ]
  %5 = icmp sgt i32 %storemerge2, 0
  br i1 %5, label %6, label %15

6:                                                ; preds = %4
  %7 = and i32 %.0, 1
  %8 = icmp eq i32 %7, 0
  %9 = lshr i32 %.0, 1
  br i1 %8, label %12, label %10

10:                                               ; preds = %6
  %11 = xor i32 %9, -306674912
  br label %13

12:                                               ; preds = %6
  br label %13

13:                                               ; preds = %12, %10
  %storemerge3 = phi i32 [ %9, %12 ], [ %11, %10 ]
  %14 = add nsw i32 %storemerge2, -1
  br label %4

15:                                               ; preds = %4
  %.0.lcssa = phi i32 [ %.0, %4 ]
  %16 = zext i32 %storemerge to i64
  %17 = getelementptr inbounds [256 x i32], [256 x i32]* @crc32_tab, i64 0, i64 %16
  store i32 %.0.lcssa, i32* %17, align 4, !tbaa !6
  %18 = add nuw nsw i32 %storemerge, 1
  br label %1

19:                                               ; preds = %1
  ret void
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @func_1() unnamed_addr #0 {
  %1 = call fastcc i8* @func_5(i32 -9, i32 -9)
  %2 = call fastcc %union.U0* @func_2(i8* @g_20, i16 signext -9)
  %3 = load volatile i32*, i32** @g_118, align 8, !tbaa !0
  %4 = load i32, i32* %3, align 4, !tbaa !6
  %5 = load i32*, i32** @g_215, align 8, !tbaa !0
  store i32 %4, i32* %5, align 4, !tbaa !6
  %6 = load volatile i16*, i16** @g_432, align 8, !tbaa !0
  %7 = load i16, i16* %6, align 2, !tbaa !9
  ret i16 %7
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc void @transparent_crc(i64 %0, i8* %1, i32 %2) unnamed_addr #0 {
  call fastcc void @crc32_8bytes(i64 %0)
  %4 = icmp eq i32 %2, 0
  br i1 %4, label %10, label %5

5:                                                ; preds = %3
  %6 = load i32, i32* @crc32_context, align 4, !tbaa !6
  %7 = xor i32 %6, -1
  %8 = zext i32 %7 to i64
  %9 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([36 x i8], [36 x i8]* @.str.24, i64 0, i64 0), i8* %1, i64 %8) #5
  br label %10

10:                                               ; preds = %5, %3
  ret void
}

declare dso_local i32 @printf(i8*, ...) local_unnamed_addr #3

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc void @platform_main_end(i32 %0, i32 %1) unnamed_addr #0 {
  %3 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([15 x i8], [15 x i8]* @.str.25, i64 0, i64 0), i32 %0) #5
  ret void
}

; Function Attrs: argmemonly nounwind willreturn
declare void @llvm.lifetime.end.p0i8(i64 immarg, i8* nocapture) #1

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc %union.U0* @func_2(i8* %0, i16 signext %1) unnamed_addr #0 {
  %3 = alloca i32, align 4
  %4 = alloca i8**, align 8
  %5 = alloca i8***, align 8
  %.sroa.0 = alloca [7 x i32], align 16
  %.sroa.5 = alloca [28 x i8], align 16
  %.sroa.6 = alloca [44 x i8], align 16
  br label %6

6:                                                ; preds = %214, %2
  %storemerge = phi i16 [ 0, %2 ], [ %218, %214 ]
  store i16 %storemerge, i16* @g_397, align 2, !tbaa !9
  %7 = icmp slt i16 %storemerge, 15
  br i1 %7, label %8, label %219

8:                                                ; preds = %6
  %9 = bitcast i32* %3 to i8*
  call void @llvm.lifetime.start.p0i8(i64 4, i8* nonnull %9) #5
  store i32 -1, i32* %3, align 4, !tbaa !6
  %10 = bitcast i8*** %4 to i8*
  call void @llvm.lifetime.start.p0i8(i64 8, i8* nonnull %10) #5
  store i8** null, i8*** %4, align 8, !tbaa !0
  %11 = bitcast i8**** %5 to i8*
  call void @llvm.lifetime.start.p0i8(i64 8, i8* nonnull %11) #5
  store i8*** %4, i8**** %5, align 8, !tbaa !0
  %12 = ptrtoint i8**** %5 to i64
  br label %13

13:                                               ; preds = %174, %8
  %.0 = phi i32 [ -326220382, %8 ], [ %.1, %174 ]
  %storemerge1 = phi i64 [ 0, %8 ], [ %213, %174 ]
  store i64 %storemerge1, i64* @g_11, align 8, !tbaa !4
  %14 = icmp eq i64 %storemerge1, 33
  br i1 %14, label %214, label %15

15:                                               ; preds = %13
  %.sroa.0.0.sroa_cast = bitcast [7 x i32]* %.sroa.0 to i8*
  call void @llvm.lifetime.start.p0i8(i64 28, i8* %.sroa.0.0.sroa_cast)
  %.sroa.5.0.sroa_idx = getelementptr inbounds [28 x i8], [28 x i8]* %.sroa.5, i64 0, i64 0
  call void @llvm.lifetime.start.p0i8(i64 28, i8* %.sroa.5.0.sroa_idx)
  %.sroa.6.0.sroa_idx = getelementptr inbounds [44 x i8], [44 x i8]* %.sroa.6, i64 0, i64 0
  call void @llvm.lifetime.start.p0i8(i64 44, i8* %.sroa.6.0.sroa_idx)
  %.sroa.0.0.sroa_cast4 = bitcast [7 x i32]* %.sroa.0 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %.sroa.0.0.sroa_cast4, i8* align 16 bitcast ([1 x [3 x [9 x i32]]]* @__const.func_2.l_509 to i8*), i64 28, i1 false)
  %.sroa.5.0.sroa_idx7 = getelementptr inbounds [28 x i8], [28 x i8]* %.sroa.5, i64 0, i64 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %.sroa.5.0.sroa_idx7, i8* align 16 bitcast (i32* getelementptr inbounds ([1 x [3 x [9 x i32]]], [1 x [3 x [9 x i32]]]* @__const.func_2.l_509, i64 0, i64 0, i64 0, i64 8) to i8*), i64 28, i1 false)
  %.sroa.6.0.sroa_idx11 = getelementptr inbounds [44 x i8], [44 x i8]* %.sroa.6, i64 0, i64 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %.sroa.6.0.sroa_idx11, i8* align 16 bitcast (i32* getelementptr inbounds ([1 x [3 x [9 x i32]]], [1 x [3 x [9 x i32]]]* @__const.func_2.l_509, i64 0, i64 0, i64 1, i64 7) to i8*), i64 44, i1 false)
  br label %16

16:                                               ; preds = %18, %15
  %storemerge2 = phi i32 [ 0, %15 ], [ %19, %18 ]
  %17 = icmp ult i32 %storemerge2, 3
  br i1 %17, label %18, label %20

18:                                               ; preds = %16
  %19 = add nuw nsw i32 %storemerge2, 1
  br label %16

20:                                               ; preds = %16
  %21 = load i8*, i8** @g_44, align 8, !tbaa !0
  %22 = load i8, i8* %21, align 1, !tbaa !8
  %23 = call fastcc i32* @func_34(i32 -9, i8* null, i16 zeroext 19979, i8 signext %22)
  %24 = load i32, i32* %3, align 4, !tbaa !6
  %25 = load i32, i32* @g_142, align 4, !tbaa !6
  %26 = icmp eq i32 %25, 1
  %27 = call fastcc signext i8 @safe_rshift_func_int8_t_s_s(i8 signext 1, i32 %24)
  %28 = icmp eq i8 %27, 0
  %29 = and i1 %28, %26
  %30 = zext i1 %29 to i32
  %31 = and i32 -1914901143, %30
  store i8 0, i8* @g_111, align 1, !tbaa !8
  %32 = call fastcc zeroext i8 @safe_rshift_func_uint8_t_u_s(i8 zeroext 0, i32 6)
  %33 = load i32, i32* @g_142, align 4, !tbaa !6
  %34 = or i32 %33, 1
  %35 = call fastcc i32 @safe_add_func_int32_t_s_s(i32 %34, i32 -1875442800)
  %36 = load i32, i32* @g_512, align 4, !tbaa !6
  %37 = icmp ult i32 %35, %36
  %38 = zext i1 %37 to i16
  %39 = load volatile i16*, i16** @g_432, align 8, !tbaa !0
  %40 = load i16, i16* %39, align 2, !tbaa !9
  %41 = sext i16 %40 to i32
  %42 = call fastcc signext i16 @safe_lshift_func_int16_t_s_s(i16 signext %38, i32 %41)
  %43 = trunc i16 %42 to i8
  %44 = call fastcc signext i8 @safe_sub_func_int8_t_s_s(i8 signext %43, i8 signext -13)
  %45 = icmp eq i8 %44, 0
  br i1 %45, label %84, label %46

46:                                               ; preds = %20
  %47 = load volatile i32, i32* @g_368, align 4, !tbaa !6
  %48 = load i8, i8* @g_20, align 1, !tbaa !8
  %49 = load i32, i32* @g_142, align 4, !tbaa !6
  %50 = trunc i32 %49 to i8
  store i8 %50, i8* @g_400, align 1, !tbaa !8
  %51 = load i32, i32* @g_512, align 4, !tbaa !6
  %52 = icmp ult i32 %31, %51
  %53 = zext i1 %52 to i32
  %54 = call fastcc i32 @safe_mod_func_uint32_t_u_u(i32 %53, i32 0)
  %55 = call fastcc signext i16 @safe_mul_func_int16_t_s_s(i16 signext 0, i16 signext -9)
  %56 = load volatile i32, i32* @g_368, align 4, !tbaa !6
  %57 = load i8*, i8** @g_44, align 8, !tbaa !0
  %58 = load i8, i8* %57, align 1, !tbaa !8
  %59 = sext i8 %58 to i32
  %60 = call fastcc signext i8 @safe_lshift_func_int8_t_s_s(i8 signext 0, i32 %59)
  %61 = sext i8 %60 to i32
  %62 = load i32, i32* @g_512, align 4, !tbaa !6
  %63 = xor i32 %62, %61
  %64 = icmp ne i32 %63, -9
  %65 = zext i1 %64 to i32
  %66 = call fastcc signext i8 @safe_rshift_func_int8_t_s_u(i8 signext %50, i32 %65)
  %67 = sext i8 %66 to i32
  %68 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 0, i64 0, i64 2), align 8, !tbaa !6
  %69 = icmp eq i32 %68, %67
  %70 = zext i1 %69 to i32
  %71 = call fastcc i32 @safe_sub_func_uint32_t_u_u(i32 %70, i32 9)
  %72 = xor i32 %71, 1444197441
  store i32 %72, i32* %3, align 4, !tbaa !6
  %73 = trunc i32 %72 to i8
  %74 = load i32, i32* @g_142, align 4, !tbaa !6
  %75 = trunc i32 %74 to i8
  %76 = call fastcc signext i8 @safe_add_func_int8_t_s_s(i8 signext %73, i8 signext %75)
  %77 = call fastcc signext i8 @safe_mod_func_int8_t_s_s(i8 signext %48, i8 signext %76)
  %78 = sext i8 %77 to i16
  %79 = call fastcc signext i16 @safe_div_func_int16_t_s_s(i16 signext 7, i16 signext %78)
  %80 = sext i16 %79 to i32
  %81 = or i32 %80, -1640375478
  %82 = and i32 %81, -9
  %83 = load volatile i32*, i32** @g_427, align 8, !tbaa !0
  store i32 %82, i32* %83, align 4, !tbaa !6
  br label %174

84:                                               ; preds = %20
  br label %85

85:                                               ; preds = %106, %84
  %.sroa.3.0 = phi i32 [ 9, %84 ], [ %137, %106 ]
  %storemerge3 = phi i32 [ 0, %84 ], [ %141, %106 ]
  store i32 %storemerge3, i32* @g_512, align 4, !tbaa !6
  %86 = icmp ult i32 %storemerge3, 55
  br i1 %86, label %87, label %142

87:                                               ; preds = %85
  store volatile i32* %3, i32** getelementptr inbounds ([6 x i32*], [6 x i32*]* @g_141, i64 0, i64 0), align 16, !tbaa !0
  %88 = load volatile i16*, i16** @g_432, align 8, !tbaa !0
  %89 = load i16, i16* %88, align 2, !tbaa !9
  %90 = call fastcc signext i16 @safe_div_func_int16_t_s_s(i16 signext -7316, i16 signext %89)
  %91 = call fastcc signext i16 @safe_div_func_int16_t_s_s(i16 signext -30891, i16 signext 0)
  %92 = and i16 %91, 229
  %93 = zext i16 %92 to i32
  %94 = load i8, i8* @g_400, align 1, !tbaa !8
  %95 = sext i8 %94 to i64
  %96 = call fastcc i64 @safe_unary_minus_func_uint64_t_u(i64 %95)
  %97 = trunc i64 %96 to i32
  %98 = load i32, i32* @g_142, align 4, !tbaa !6
  %99 = trunc i32 %98 to i16
  %100 = load i8*, i8** @g_44, align 8, !tbaa !0
  %101 = load i8, i8* %100, align 1, !tbaa !8
  %102 = call fastcc i32* @func_34(i32 %97, i8* null, i16 zeroext %99, i8 signext %101)
  br i1 false, label %106, label %103

103:                                              ; preds = %87
  %104 = load i32, i32* @g_142, align 4, !tbaa !6
  %105 = icmp ne i32 %104, 0
  br label %106

106:                                              ; preds = %103, %87
  %107 = phi i1 [ undef, %87 ], [ %105, %103 ]
  %108 = zext i1 %107 to i32
  %109 = call fastcc i32 @safe_mod_func_uint32_t_u_u(i32 %93, i32 %108)
  %110 = call fastcc i32 @safe_add_func_uint32_t_u_u(i32 %109, i32 2)
  %111 = call fastcc signext i16 @safe_mul_func_int16_t_s_s(i16 signext 1, i16 signext -9)
  %112 = load i32*, i32** @g_215, align 8, !tbaa !0
  store i32 1, i32* %112, align 4, !tbaa !6
  %113 = load i32, i32* @g_512, align 4, !tbaa !6
  %114 = zext i32 %113 to i64
  %115 = load volatile i32*, i32** @g_118, align 8, !tbaa !0
  %116 = load i32, i32* %115, align 4, !tbaa !6
  %117 = load i32, i32* @g_142, align 4, !tbaa !6
  %118 = add i32 %117, 1
  store i32 %118, i32* @g_142, align 4, !tbaa !6
  %119 = call fastcc zeroext i8 @safe_mod_func_uint8_t_u_u(i8 zeroext -9, i8 zeroext 1)
  %120 = zext i8 %119 to i64
  store i64 %120, i64* @g_575, align 8, !tbaa !4
  %121 = icmp slt i32 %116, 1
  %122 = zext i1 %121 to i32
  %123 = and i32 %122, -9
  %124 = zext i32 %123 to i64
  %125 = load i64, i64* @g_11, align 8, !tbaa !4
  %126 = or i64 %125, %124
  %127 = icmp ugt i64 %126, %114
  %128 = zext i1 %127 to i8
  %129 = call fastcc signext i8 @safe_unary_minus_func_int8_t_s(i8 signext %128)
  %130 = sext i8 %129 to i16
  %131 = load i32, i32* @g_172, align 4, !tbaa !6
  %132 = icmp ugt i32 %131, -14818
  %133 = zext i1 %132 to i8
  %134 = call fastcc signext i8 @safe_unary_minus_func_int8_t_s(i8 signext %133)
  %135 = call fastcc i32 @safe_sub_func_uint32_t_u_u(i32 1, i32 -9)
  %136 = call fastcc signext i16 @safe_rshift_func_int16_t_s_u(i16 signext %130, i32 %135)
  %137 = and i32 %.sroa.3.0, 1
  store i32 -9, i32* @g_142, align 4, !tbaa !6
  %138 = load i32, i32* @g_512, align 4, !tbaa !6
  %139 = trunc i32 %138 to i8
  %140 = call fastcc zeroext i8 @safe_add_func_uint8_t_u_u(i8 zeroext %139, i8 zeroext 1)
  %141 = zext i8 %140 to i32
  br label %85

142:                                              ; preds = %85
  %143 = load volatile i16*, i16** @g_432, align 8, !tbaa !0
  %144 = load i16, i16* %143, align 2, !tbaa !9
  %145 = load i16, i16* @g_140, align 2, !tbaa !9
  %146 = xor i16 %145, %144
  store i16 %146, i16* @g_140, align 2, !tbaa !9
  %147 = call fastcc signext i16 @safe_sub_func_int16_t_s_s(i16 signext %146, i16 signext 1)
  %148 = icmp sgt i16 %147, 0
  %149 = load i8, i8* @g_111, align 1, !tbaa !8
  %150 = add i8 %149, -1
  store i8 %150, i8* @g_111, align 1, !tbaa !8
  %151 = zext i8 %150 to i64
  %152 = load i32, i32* @g_172, align 4, !tbaa !6
  %153 = trunc i32 %152 to i8
  %154 = call fastcc zeroext i8 @safe_mul_func_uint8_t_u_u(i8 zeroext %153, i8 zeroext 0)
  %155 = call fastcc signext i16 @safe_lshift_func_int16_t_s_u(i16 signext 0, i32 15)
  %156 = load i32, i32* @g_142, align 4, !tbaa !6
  %157 = call fastcc zeroext i8 @safe_lshift_func_uint8_t_u_u(i8 zeroext 0, i32 %156)
  %158 = call fastcc signext i8 @safe_sub_func_int8_t_s_s(i8 signext 0, i8 signext 0)
  %159 = call fastcc signext i16 @safe_lshift_func_int16_t_s_s(i16 signext 1, i32 13)
  %160 = sext i16 %159 to i64
  %161 = load i64, i64* @g_11, align 8, !tbaa !4
  %162 = or i64 %161, %160
  %163 = icmp ugt i64 %162, %151
  %164 = and i1 %148, %163
  %165 = zext i1 %164 to i32
  %166 = load i8, i8* @g_400, align 1, !tbaa !8
  %167 = sext i8 %166 to i32
  %168 = icmp sgt i32 %165, %167
  %169 = zext i1 %168 to i64
  %170 = load i8, i8* @g_20, align 1, !tbaa !8
  %171 = sext i8 %170 to i64
  %172 = call fastcc i64 @safe_mod_func_uint64_t_u_u(i64 %169, i64 %171)
  store i32 1, i32* @g_142, align 4, !tbaa !6
  %173 = or i32 %.0, 1
  br label %174

174:                                              ; preds = %142, %46
  %.1 = phi i32 [ %173, %142 ], [ %.0, %46 ]
  %175 = load i8*, i8** @g_44, align 8, !tbaa !0
  %176 = load i8, i8* %175, align 1, !tbaa !8
  %177 = load i64, i64* @g_575, align 8, !tbaa !4
  %178 = add i64 %177, -1
  store i64 %178, i64* @g_575, align 8, !tbaa !4
  %179 = load i64, i64* getelementptr inbounds ([4 x i64], [4 x i64]* @g_131, i64 0, i64 1), align 8, !tbaa !4
  store i64 %179, i64* getelementptr inbounds ([4 x i64], [4 x i64]* @g_131, i64 0, i64 3), align 8, !tbaa !4
  %180 = icmp ule i64 %178, %179
  %181 = zext i1 %180 to i16
  %182 = load i16, i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 4), align 8, !tbaa !9
  %183 = trunc i16 %182 to i8
  store i8 %183, i8* @g_111, align 1, !tbaa !8
  %184 = call fastcc zeroext i8 @safe_mod_func_uint8_t_u_u(i8 zeroext 0, i8 zeroext 8)
  %185 = zext i8 %184 to i32
  store i32 %185, i32* @g_142, align 4, !tbaa !6
  %186 = call fastcc zeroext i8 @safe_lshift_func_uint8_t_u_u(i8 zeroext 1, i32 -9)
  %187 = zext i8 %186 to i16
  %188 = or i16 -9, %187
  %189 = load i16, i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 7), align 2, !tbaa !9
  %190 = or i16 %188, %189
  %191 = call fastcc signext i16 @safe_sub_func_int16_t_s_s(i16 signext %181, i16 signext %190)
  %192 = call fastcc i64 @safe_div_func_int64_t_s_s(i64 1, i64 2)
  %193 = trunc i64 %192 to i16
  %194 = load volatile i16*, i16** @g_432, align 8, !tbaa !0
  %195 = load i16, i16* %194, align 2, !tbaa !9
  %196 = call fastcc zeroext i16 @safe_mul_func_uint16_t_u_u(i16 zeroext %193, i16 zeroext %195)
  %197 = zext i16 %196 to i32
  %198 = call fastcc i32 @safe_mod_func_int32_t_s_s(i32 -9, i32 %197)
  %199 = call fastcc i32 @safe_add_func_int32_t_s_s(i32 %198, i32 %.1)
  %200 = trunc i32 %199 to i8
  %201 = load i8*, i8** @g_44, align 8, !tbaa !0
  %202 = load i8, i8* %201, align 1, !tbaa !8
  %203 = sext i8 %202 to i32
  %204 = call fastcc signext i8 @safe_rshift_func_int8_t_s_s(i8 signext %200, i32 %203)
  %205 = load i8*, i8** @g_44, align 8, !tbaa !0
  %206 = load i8, i8* %205, align 1, !tbaa !8
  %207 = sext i8 %206 to i32
  %208 = call fastcc signext i8 @safe_rshift_func_int8_t_s_s(i8 signext %176, i32 %207)
  %209 = icmp eq i8 %208, 0
  %210 = zext i1 %209 to i32
  %211 = call fastcc i32 @safe_div_func_int32_t_s_s(i32 %210, i32 1)
  store i64 %12, i64* bitcast (i8***** @g_635 to i64*), align 8, !tbaa !0
  %.sroa.0.0.sroa_cast23 = bitcast [7 x i32]* %.sroa.0 to i8*
  call void @llvm.lifetime.end.p0i8(i64 28, i8* %.sroa.0.0.sroa_cast23)
  %.sroa.5.0.sroa_idx22 = getelementptr inbounds [28 x i8], [28 x i8]* %.sroa.5, i64 0, i64 0
  call void @llvm.lifetime.end.p0i8(i64 28, i8* %.sroa.5.0.sroa_idx22)
  %.sroa.6.0.sroa_idx21 = getelementptr inbounds [44 x i8], [44 x i8]* %.sroa.6, i64 0, i64 0
  call void @llvm.lifetime.end.p0i8(i64 44, i8* %.sroa.6.0.sroa_idx21)
  %212 = load i64, i64* @g_11, align 8, !tbaa !4
  %213 = add i64 %212, 1
  br label %13

214:                                              ; preds = %13
  call void @llvm.lifetime.end.p0i8(i64 8, i8* nonnull %11) #5
  call void @llvm.lifetime.end.p0i8(i64 8, i8* nonnull %10) #5
  call void @llvm.lifetime.end.p0i8(i64 4, i8* nonnull %9) #5
  %215 = load i16, i16* @g_397, align 2, !tbaa !9
  %216 = sext i16 %215 to i64
  %217 = call fastcc i64 @safe_add_func_int64_t_s_s(i64 %216, i64 2)
  %218 = trunc i64 %217 to i16
  br label %6

219:                                              ; preds = %6
  ret %union.U0* undef
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i8* @func_5(i32 %0, i32 %1) unnamed_addr #0 {
  br label %3

3:                                                ; preds = %5, %2
  %storemerge = phi i32 [ 0, %2 ], [ %6, %5 ]
  %4 = icmp ult i32 %storemerge, 2
  br i1 %4, label %5, label %7

5:                                                ; preds = %3
  %6 = add nuw nsw i32 %storemerge, 1
  br label %3

7:                                                ; preds = %3
  %8 = load i32, i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 7), align 4, !tbaa !6
  %9 = call fastcc i32 @safe_sub_func_uint32_t_u_u(i32 -729453352, i32 %8)
  %10 = trunc i32 %9 to i8
  %11 = call fastcc i8* @func_30(i8 zeroext %10)
  %12 = call fastcc i8* @func_24(i16 signext 1, i16 zeroext -9, i32 27)
  %13 = call fastcc i32* @func_12(i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 8), i8* nonnull @g_20, i32* null, i8* @g_20)
  ret i8* undef
}

; Function Attrs: argmemonly nounwind willreturn
declare void @llvm.memset.p0i8.i64(i8* nocapture writeonly, i8, i64, i1 immarg) #1

; Function Attrs: argmemonly nounwind willreturn
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* noalias nocapture writeonly, i8* noalias nocapture readonly, i64, i1 immarg) #1

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i32* @func_34(i32 %0, i8* %1, i16 zeroext %2, i8 signext %3) unnamed_addr #0 {
  br label %5

5:                                                ; preds = %6, %4
  %phiofops = phi i1 [ true, %4 ], [ false, %6 ]
  br i1 %phiofops, label %6, label %7

6:                                                ; preds = %5
  br label %5

7:                                                ; preds = %5
  %8 = trunc i32 -350089660 to i8
  store i8 %8, i8* @g_111, align 1, !tbaa !8
  %9 = call fastcc zeroext i8 @safe_rshift_func_uint8_t_u_u(i8 zeroext %8, i32 6)
  br label %10

10:                                               ; preds = %7
  %11 = call fastcc signext i16 @safe_mul_func_int16_t_s_s(i16 signext 1, i16 signext 3954)
  %12 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 1, i64 0, i64 0), align 4, !tbaa !6
  %13 = or i32 %12, -350089660
  store i32 %13, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 1, i64 0, i64 0), align 4, !tbaa !6
  ret i32* undef
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_sub_func_int8_t_s_s(i8 signext %0, i8 signext %1) unnamed_addr #0 {
  %3 = sub i8 %0, %1
  ret i8 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @safe_lshift_func_int16_t_s_s(i16 signext %0, i32 %1) unnamed_addr #0 {
  %3 = sext i16 %0 to i32
  %4 = icmp slt i16 %0, 0
  %5 = icmp ugt i32 %1, 31
  %6 = or i1 %5, %4
  %7 = lshr i32 32767, %1
  %8 = icmp slt i32 %7, %3
  %or.cond3 = or i1 %6, %8
  %9 = select i1 %or.cond3, i32 0, i32 %1
  %10 = shl i32 %3, %9
  %11 = trunc i32 %10 to i16
  ret i16 %11
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i32 @safe_add_func_int32_t_s_s(i32 %0, i32 %1) unnamed_addr #0 {
  %3 = icmp sgt i32 %0, 0
  %4 = icmp sgt i32 %1, 0
  %or.cond = and i1 %3, %4
  %5 = sub nsw i32 2147483647, %1
  %6 = icmp slt i32 %5, %0
  %or.cond2 = and i1 %or.cond, %6
  br i1 %or.cond2, label %13, label %7

7:                                                ; preds = %2
  %8 = icmp slt i32 %0, 0
  br i1 %8, label %9, label %14

9:                                                ; preds = %7
  %10 = icmp slt i32 %1, 0
  %11 = sub nsw i32 -2147483648, %1
  %12 = icmp sgt i32 %11, %0
  %or.cond4 = and i1 %10, %12
  br i1 %or.cond4, label %13, label %14

13:                                               ; preds = %9, %2
  br label %16

14:                                               ; preds = %9, %7
  %15 = add nsw i32 %0, %1
  br label %16

16:                                               ; preds = %14, %13
  %17 = phi i32 [ %0, %13 ], [ %15, %14 ]
  ret i32 %17
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i8 @safe_rshift_func_uint8_t_u_s(i8 zeroext %0, i32 %1) unnamed_addr #0 {
  %3 = zext i8 %0 to i32
  %4 = lshr i32 %3, 6
  %5 = trunc i32 %4 to i8
  ret i8 %5
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_rshift_func_int8_t_s_s(i8 signext %0, i32 %1) unnamed_addr #0 {
  %3 = sext i8 %0 to i32
  %4 = icmp slt i8 %0, 0
  %5 = icmp ugt i32 %1, 31
  %6 = or i1 %5, %4
  %7 = select i1 %6, i32 0, i32 %1
  %8 = ashr i32 %3, %7
  %9 = trunc i32 %8 to i8
  ret i8 %9
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @safe_div_func_int16_t_s_s(i16 signext %0, i16 signext %1) unnamed_addr #0 {
  %3 = sext i16 %1 to i32
  %4 = icmp eq i16 %1, 0
  br i1 %4, label %8, label %5

5:                                                ; preds = %2
  %6 = icmp eq i16 %0, -32768
  %7 = icmp eq i16 %1, -1
  %or.cond = and i1 %6, %7
  br i1 %or.cond, label %8, label %10

8:                                                ; preds = %5, %2
  %9 = sext i16 %0 to i32
  br label %13

10:                                               ; preds = %5
  %11 = sext i16 %0 to i32
  %12 = sdiv i32 %11, %3
  br label %13

13:                                               ; preds = %10, %8
  %14 = phi i32 [ %9, %8 ], [ %12, %10 ]
  %15 = trunc i32 %14 to i16
  ret i16 %15
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_mod_func_int8_t_s_s(i8 signext %0, i8 signext %1) unnamed_addr #0 {
  %3 = sext i8 %1 to i32
  %4 = icmp eq i8 %1, 0
  br i1 %4, label %8, label %5

5:                                                ; preds = %2
  %6 = icmp eq i8 %0, -128
  %7 = icmp eq i8 %1, -1
  %or.cond = and i1 %6, %7
  br i1 %or.cond, label %8, label %10

8:                                                ; preds = %5, %2
  %9 = sext i8 %0 to i32
  br label %13

10:                                               ; preds = %5
  %11 = sext i8 %0 to i32
  %12 = srem i32 %11, %3
  br label %13

13:                                               ; preds = %10, %8
  %14 = phi i32 [ %9, %8 ], [ %12, %10 ]
  %15 = trunc i32 %14 to i8
  ret i8 %15
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_add_func_int8_t_s_s(i8 signext %0, i8 signext %1) unnamed_addr #0 {
  %3 = add i8 %0, %1
  ret i8 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i32 @safe_sub_func_uint32_t_u_u(i32 %0, i32 %1) unnamed_addr #0 {
  %3 = sub i32 %0, %1
  ret i32 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_rshift_func_int8_t_s_u(i8 signext %0, i32 %1) unnamed_addr #0 {
  %3 = sext i8 %0 to i32
  %4 = icmp slt i8 %0, 0
  %5 = icmp ugt i32 %1, 31
  %or.cond = or i1 %4, %5
  %6 = select i1 %or.cond, i32 0, i32 %1
  %7 = ashr i32 %3, %6
  %8 = trunc i32 %7 to i8
  ret i8 %8
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_lshift_func_int8_t_s_s(i8 signext %0, i32 %1) unnamed_addr #0 {
  %3 = sext i8 %0 to i32
  %4 = icmp slt i8 %0, 0
  %5 = icmp ugt i32 %1, 31
  %6 = or i1 %5, %4
  %7 = lshr i32 127, %1
  %8 = icmp slt i32 %7, %3
  %or.cond3 = or i1 %6, %8
  %9 = select i1 %or.cond3, i32 0, i32 %1
  %10 = shl i32 %3, %9
  %11 = trunc i32 %10 to i8
  ret i8 %11
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @safe_mul_func_int16_t_s_s(i16 signext %0, i16 signext %1) unnamed_addr #0 {
  %3 = mul i16 %0, %1
  ret i16 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i32 @safe_mod_func_uint32_t_u_u(i32 %0, i32 %1) unnamed_addr #0 {
  %3 = icmp eq i32 %1, 0
  br i1 %3, label %6, label %4

4:                                                ; preds = %2
  %5 = urem i32 %0, %1
  br label %6

6:                                                ; preds = %4, %2
  %7 = phi i32 [ %5, %4 ], [ %0, %2 ]
  ret i32 %7
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i32 @safe_add_func_uint32_t_u_u(i32 %0, i32 %1) unnamed_addr #0 {
  %3 = add i32 %0, 2
  ret i32 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i64 @safe_unary_minus_func_uint64_t_u(i64 %0) unnamed_addr #0 {
  %2 = sub i64 0, %0
  ret i64 %2
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @safe_rshift_func_int16_t_s_u(i16 signext %0, i32 %1) unnamed_addr #0 {
  %3 = sext i16 %0 to i32
  %4 = icmp slt i16 %0, 0
  %5 = icmp ugt i32 %1, 31
  %or.cond = or i1 %4, %5
  %6 = select i1 %or.cond, i32 0, i32 %1
  %7 = ashr i32 %3, %6
  %8 = trunc i32 %7 to i16
  ret i16 %8
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_unary_minus_func_int8_t_s(i8 signext %0) unnamed_addr #0 {
  %2 = sub i8 0, %0
  ret i8 %2
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i8 @safe_mod_func_uint8_t_u_u(i8 zeroext %0, i8 zeroext %1) unnamed_addr #0 {
  %3 = icmp eq i8 %1, 0
  br i1 %3, label %6, label %4

4:                                                ; preds = %2
  %5 = urem i8 %0, %1
  br label %6

6:                                                ; preds = %4, %2
  %.in = phi i8 [ %5, %4 ], [ %0, %2 ]
  ret i8 %.in
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i8 @safe_add_func_uint8_t_u_u(i8 zeroext %0, i8 zeroext %1) unnamed_addr #0 {
  %3 = add i8 %0, %1
  ret i8 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i64 @safe_mod_func_uint64_t_u_u(i64 %0, i64 %1) unnamed_addr #0 {
  %3 = icmp eq i64 %1, 0
  br i1 %3, label %6, label %4

4:                                                ; preds = %2
  %5 = urem i64 %0, %1
  br label %6

6:                                                ; preds = %4, %2
  %7 = phi i64 [ %5, %4 ], [ %0, %2 ]
  ret i64 %7
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @safe_sub_func_int16_t_s_s(i16 signext %0, i16 signext %1) unnamed_addr #0 {
  %3 = sub i16 %0, %1
  ret i16 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i8 @safe_mul_func_uint8_t_u_u(i8 zeroext %0, i8 zeroext %1) unnamed_addr #0 {
  %3 = mul i8 %0, %1
  ret i8 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i8 @safe_lshift_func_uint8_t_u_u(i8 zeroext %0, i32 %1) unnamed_addr #0 {
  %3 = icmp ugt i32 %1, 31
  %4 = zext i8 %0 to i32
  br i1 %3, label %8, label %5

5:                                                ; preds = %2
  %6 = lshr i32 255, %1
  %7 = icmp slt i32 %6, %4
  br i1 %7, label %8, label %9

8:                                                ; preds = %5, %2
  br label %11

9:                                                ; preds = %5
  %10 = shl i32 %4, %1
  br label %11

11:                                               ; preds = %9, %8
  %12 = phi i32 [ %4, %8 ], [ %10, %9 ]
  %13 = trunc i32 %12 to i8
  ret i8 %13
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @safe_lshift_func_int16_t_s_u(i16 signext %0, i32 %1) unnamed_addr #0 {
  ret i16 undef
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i32 @safe_div_func_int32_t_s_s(i32 %0, i32 %1) unnamed_addr #0 {
  br label %3

3:                                                ; preds = %2
  br label %4

4:                                                ; preds = %3
  br label %5

5:                                                ; preds = %4
  ret i32 %0
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i32 @safe_mod_func_int32_t_s_s(i32 %0, i32 %1) unnamed_addr #0 {
  %3 = icmp eq i32 %1, 0
  br i1 %3, label %7, label %4

4:                                                ; preds = %2
  %5 = icmp eq i32 %0, -2147483648
  %6 = icmp eq i32 %1, -1
  %or.cond = and i1 %5, %6
  br i1 %or.cond, label %7, label %8

7:                                                ; preds = %4, %2
  br label %10

8:                                                ; preds = %4
  %9 = srem i32 %0, %1
  br label %10

10:                                               ; preds = %8, %7
  %11 = phi i32 [ %0, %7 ], [ %9, %8 ]
  ret i32 %11
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i16 @safe_mul_func_uint16_t_u_u(i16 zeroext %0, i16 zeroext %1) unnamed_addr #0 {
  %3 = mul i16 %0, %1
  ret i16 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i64 @safe_div_func_int64_t_s_s(i64 %0, i64 %1) unnamed_addr #0 {
  br label %3

3:                                                ; preds = %2
  br label %4

4:                                                ; preds = %3
  %5 = sdiv i64 %0, 2
  br label %6

6:                                                ; preds = %4
  ret i64 %5
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i64 @safe_add_func_int64_t_s_s(i64 %0, i64 %1) unnamed_addr #0 {
  %3 = icmp sgt i64 %0, 0
  %4 = icmp slt i64 9223372036854775805, %0
  %or.cond2 = and i1 %3, %4
  br i1 %or.cond2, label %7, label %5

5:                                                ; preds = %2
  br label %8

6:                                                ; No predecessors!
  br label %8

7:                                                ; preds = %2
  br label %10

8:                                                ; preds = %6, %5
  %9 = add nsw i64 %0, 2
  br label %10

10:                                               ; preds = %8, %7
  %11 = phi i64 [ %0, %7 ], [ %9, %8 ]
  ret i64 %11
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i8 @safe_rshift_func_uint8_t_u_u(i8 zeroext %0, i32 %1) unnamed_addr #0 {
  %3 = icmp ugt i32 %1, 31
  %4 = zext i8 %0 to i32
  %5 = select i1 %3, i32 0, i32 %1
  %6 = lshr i32 %4, %5
  %7 = trunc i32 %6 to i8
  ret i8 %7
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_mul_func_int8_t_s_s(i8 signext %0, i8 signext %1) unnamed_addr #0 {
  %3 = mul i8 %0, %1
  ret i8 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i32* @func_12(i32* %0, i8* %1, i32* %2, i8* %3) unnamed_addr #0 {
  %5 = alloca [2 x i32], align 4
  br label %6

6:                                                ; preds = %71, %4
  store i16 21, i16* @g_140, align 2, !tbaa !9
  br i1 true, label %7, label %72

7:                                                ; preds = %6
  %8 = bitcast [2 x i32]* %5 to i8*
  call void @llvm.lifetime.start.p0i8(i64 8, i8* nonnull %8) #5
  br label %9

9:                                                ; preds = %11, %7
  %storemerge6 = phi i32 [ 0, %7 ], [ %14, %11 ]
  %10 = icmp ult i32 %storemerge6, 2
  br i1 %10, label %11, label %15

11:                                               ; preds = %9
  %12 = zext i32 %storemerge6 to i64
  %13 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 %12
  store i32 9, i32* %13, align 4, !tbaa !6
  %14 = add nuw nsw i32 %storemerge6, 1
  br label %9

15:                                               ; preds = %9
  %16 = load i64, i64* @g_11, align 8, !tbaa !4
  %17 = add i64 %16, -1
  store i64 %17, i64* @g_11, align 8, !tbaa !4
  %18 = call fastcc i64 @safe_unary_minus_func_uint64_t_u(i64 %17)
  %19 = xor i64 %18, 3
  %20 = load i64, i64* getelementptr inbounds ([4 x i64], [4 x i64]* @g_131, i64 0, i64 1), align 8, !tbaa !4
  %21 = trunc i64 %20 to i16
  %22 = call fastcc signext i8 @safe_mul_func_int8_t_s_s(i8 signext 1, i8 signext 64)
  %23 = icmp eq i8 %22, 2
  %24 = zext i1 %23 to i8
  %25 = load i64, i64* getelementptr inbounds ([4 x i64], [4 x i64]* @g_131, i64 0, i64 2), align 16, !tbaa !4
  %26 = trunc i64 %25 to i8
  %27 = call fastcc signext i8 @safe_div_func_int8_t_s_s(i8 signext %24, i8 signext %26)
  %28 = sext i8 %27 to i32
  %29 = load i32, i32* @g_171, align 4, !tbaa !6
  %30 = call fastcc i32 @safe_div_func_uint32_t_u_u(i32 %28, i32 %29)
  %31 = load i8*, i8** @g_44, align 8, !tbaa !0
  %32 = load i8, i8* %31, align 1, !tbaa !8
  %33 = icmp ne i8 %32, 0
  %34 = zext i1 %33 to i32
  %35 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 0
  %36 = load i32, i32* %35, align 4, !tbaa !6
  %37 = xor i32 %36, %34
  %38 = call fastcc zeroext i16 @safe_rshift_func_uint16_t_u_u(i16 zeroext %21, i32 %37)
  %39 = zext i16 %38 to i64
  %40 = call fastcc i64 @safe_unary_minus_func_uint64_t_u(i64 %39)
  %41 = icmp eq i64 %40, 9
  %42 = zext i1 %41 to i64
  %43 = xor i64 %19, %42
  %44 = trunc i64 %43 to i8
  %45 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 1
  %46 = load i32, i32* %45, align 4, !tbaa !6
  %47 = trunc i32 %46 to i8
  %48 = call fastcc zeroext i8 @safe_mul_func_uint8_t_u_u(i8 zeroext %44, i8 zeroext %47)
  %49 = load i16, i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 6), align 4, !tbaa !9
  %50 = zext i16 %49 to i64
  %51 = trunc i32 %36 to i16
  %52 = call fastcc signext i16 @safe_mul_func_int16_t_s_s(i16 signext -18902, i16 signext %51)
  %53 = icmp ne i16 %52, 0
  %54 = zext i1 %53 to i16
  %55 = trunc i32 %46 to i16
  %56 = call fastcc i8* @func_24(i16 signext %54, i16 zeroext %55, i32 65535)
  %57 = call fastcc i8* @func_39(i64 %50, i8** nonnull @g_44, i8* @g_20)
  %58 = call fastcc i32 @safe_mod_func_uint32_t_u_u(i32 %46, i32 833339902)
  %59 = icmp ne i32 %58, 0
  %60 = load i8, i8* @g_20, align 1
  %61 = icmp ne i8 %60, 0
  %62 = or i1 %61, %59
  %63 = zext i1 %62 to i8
  %64 = call fastcc zeroext i8 @safe_mod_func_uint8_t_u_u(i8 zeroext 42, i8 zeroext %63)
  store i32 1, i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 8), align 4, !tbaa !6
  br label %65

65:                                               ; preds = %15
  br label %68

66:                                               ; No predecessors!
  br label %67

67:                                               ; preds = %66
  unreachable

68:                                               ; preds = %65
  br label %70

69:                                               ; No predecessors!
  unreachable

70:                                               ; preds = %68
  call void @llvm.lifetime.end.p0i8(i64 8, i8* nonnull %8) #5
  switch i32 2, label %.loopexit.loopexit [
    i32 0, label %71
    i32 2, label %72
  ]

71:                                               ; preds = %70
  br label %6

72:                                               ; preds = %70, %6
  br label %73

73:                                               ; preds = %72
  br label %74

74:                                               ; preds = %73
  br label %.loopexit

.loopexit.loopexit:                               ; preds = %70
  br label %.loopexit

.loopexit:                                        ; preds = %.loopexit.loopexit, %74
  ret i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 4)
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i8* @func_24(i16 signext %0, i16 zeroext %1, i32 %2) unnamed_addr #0 {
  ret i8* undef
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i8* @func_30(i8 zeroext %0) unnamed_addr #0 {
  %2 = alloca [4 x i32], align 16
  %3 = alloca i8, align 1
  %4 = bitcast [4 x i32]* %2 to i8*
  call void @llvm.lifetime.start.p0i8(i64 16, i8* nonnull %4) #5
  call void @llvm.lifetime.start.p0i8(i64 1, i8* nonnull %3) #5
  store i8 -5, i8* %3, align 1, !tbaa !8
  %5 = getelementptr inbounds [4 x i32], [4 x i32]* %2, i64 0, i64 1
  br label %6

6:                                                ; preds = %8, %1
  %storemerge = phi i32 [ 0, %1 ], [ %11, %8 ]
  %7 = icmp ult i32 %storemerge, 4
  br i1 %7, label %8, label %12

8:                                                ; preds = %6
  %9 = zext i32 %storemerge to i64
  %10 = getelementptr inbounds [4 x i32], [4 x i32]* %2, i64 0, i64 %9
  store i32 -4, i32* %10, align 4, !tbaa !6
  %11 = add nuw nsw i32 %storemerge, 1
  br label %6

12:                                               ; preds = %6
  br label %13

13:                                               ; preds = %25, %12
  %storemerge4 = phi i32 [ 0, %12 ], [ %26, %25 ]
  %14 = icmp ult i32 %storemerge4, 2
  br i1 %14, label %15, label %27

15:                                               ; preds = %13
  br label %16

16:                                               ; preds = %23, %15
  %storemerge5 = phi i32 [ 0, %15 ], [ %24, %23 ]
  %17 = icmp ult i32 %storemerge5, 4
  br i1 %17, label %18, label %25

18:                                               ; preds = %16
  br label %19

19:                                               ; preds = %21, %18
  %storemerge6 = phi i32 [ 0, %18 ], [ %22, %21 ]
  %20 = icmp ult i32 %storemerge6, 2
  br i1 %20, label %21, label %23

21:                                               ; preds = %19
  %22 = add nuw nsw i32 %storemerge6, 1
  br label %19

23:                                               ; preds = %19
  %24 = add nuw nsw i32 %storemerge5, 1
  br label %16

25:                                               ; preds = %16
  %26 = add nuw nsw i32 %storemerge4, 1
  br label %13

27:                                               ; preds = %13
  %28 = zext i8 %0 to i64
  %29 = call fastcc i8* @func_39(i64 %28, i8** nonnull @g_44, i8* null)
  %30 = load i32, i32* @g_171, align 4, !tbaa !6
  %31 = sext i32 %30 to i64
  %32 = call fastcc i64 @safe_sub_func_int64_t_s_s(i64 1, i64 %31)
  %33 = trunc i64 %32 to i32
  %34 = getelementptr inbounds [4 x i32], [4 x i32]* %2, i64 0, i64 2
  %35 = load i32, i32* %34, align 8, !tbaa !6
  %36 = trunc i32 %35 to i16
  %37 = load i8, i8* %3, align 1, !tbaa !8
  %38 = call fastcc i32* @func_34(i32 %33, i8* null, i16 zeroext %36, i8 signext %37)
  store i32* @g_142, i32** @g_215, align 8, !tbaa !0
  store volatile i32* @g_142, i32** getelementptr inbounds ([7 x [2 x i32*]], [7 x [2 x i32*]]* @g_211, i64 0, i64 4, i64 1), align 8, !tbaa !0
  %39 = load i32, i32* %5, align 4, !tbaa !6
  store i32 %39, i32* @g_142, align 4, !tbaa !6
  br i1 icmp eq (i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 1), i16* inttoptr (i64 trunc (i128 lshr (i128 bitcast (<2 x i64> <i64 ptrtoint (i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 7) to i64), i64 ptrtoint (i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 7) to i64)> to i128), i128 64) to i64) to i16*)), label %40, label %53

40:                                               ; preds = %27
  %41 = load i16, i16* @g_58, align 2, !tbaa !9
  %42 = trunc i16 %41 to i8
  %43 = load i8, i8* @g_111, align 1, !tbaa !8
  %44 = and i8 %43, %42
  store i8 %44, i8* @g_111, align 1, !tbaa !8
  %45 = call fastcc zeroext i8 @safe_add_func_uint8_t_u_u(i8 zeroext -103, i8 zeroext %44)
  %46 = zext i8 %45 to i16
  store i16 %46, i16* @g_58, align 2, !tbaa !9
  %47 = zext i8 %0 to i16
  %48 = call fastcc signext i16 @safe_mul_func_int16_t_s_s(i16 signext %46, i16 signext %47)
  %49 = call fastcc zeroext i16 @safe_mod_func_uint16_t_u_u(i16 zeroext %47, i16 zeroext 4)
  %50 = trunc i16 %49 to i8
  %51 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 1, i64 0, i64 0), align 4, !tbaa !6
  %52 = call fastcc signext i8 @safe_lshift_func_int8_t_s_u(i8 signext %50, i32 %51)
  br label %53

53:                                               ; preds = %40, %27
  %54 = phi i64 [ -7, %27 ], [ -8, %40 ]
  store i64 %54, i64* @g_11, align 8, !tbaa !4
  %55 = call fastcc i8* @func_39(i64 %54, i8** nonnull @g_44, i8* nonnull %3)
  %56 = call fastcc signext i8 @safe_rshift_func_int8_t_s_s(i8 signext 0, i32 1)
  %57 = trunc i32 %39 to i8
  %58 = call fastcc signext i8 @safe_unary_minus_func_int8_t_s(i8 signext %57)
  %59 = sext i8 %58 to i32
  %60 = load volatile i32*, i32** @g_118, align 8, !tbaa !0
  store i32 %59, i32* %60, align 4, !tbaa !6
  call void @llvm.lifetime.end.p0i8(i64 1, i8* nonnull %3) #5
  call void @llvm.lifetime.end.p0i8(i64 16, i8* nonnull %4) #5
  ret i8* undef
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @safe_mod_func_int16_t_s_s(i16 signext %0, i16 signext %1) unnamed_addr #0 {
  br label %3

3:                                                ; preds = %2
  br label %4

4:                                                ; preds = %3
  br label %5

5:                                                ; preds = %4
  ret i16 undef
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @safe_rshift_func_int16_t_s_s(i16 signext %0, i32 %1) unnamed_addr #0 {
  %3 = sext i16 %0 to i32
  %4 = icmp slt i16 %0, 0
  %5 = icmp ugt i32 %1, 31
  %6 = or i1 %5, %4
  %7 = select i1 %6, i32 0, i32 %1
  %8 = ashr i32 %3, %7
  %9 = trunc i32 %8 to i16
  ret i16 %9
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i16 @safe_add_func_uint16_t_u_u(i16 zeroext %0, i16 zeroext %1) unnamed_addr #0 {
  %3 = add i16 %0, 27281
  ret i16 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i16 @safe_rshift_func_uint16_t_u_u(i16 zeroext %0, i32 %1) unnamed_addr #0 {
  %3 = icmp ugt i32 %1, 31
  %4 = zext i16 %0 to i32
  %5 = select i1 %3, i32 0, i32 %1
  %6 = lshr i32 %4, %5
  %7 = trunc i32 %6 to i16
  ret i16 %7
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i32 @safe_div_func_uint32_t_u_u(i32 %0, i32 %1) unnamed_addr #0 {
  %3 = icmp eq i32 %1, 0
  br i1 %3, label %6, label %4

4:                                                ; preds = %2
  %5 = udiv i32 %0, %1
  br label %6

6:                                                ; preds = %4, %2
  %7 = phi i32 [ %5, %4 ], [ %0, %2 ]
  ret i32 %7
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_div_func_int8_t_s_s(i8 signext %0, i8 signext %1) unnamed_addr #0 {
  %3 = sext i8 %1 to i32
  %4 = icmp eq i8 %1, 0
  br i1 %4, label %8, label %5

5:                                                ; preds = %2
  %6 = icmp eq i8 %0, -128
  %7 = icmp eq i8 %1, -1
  %or.cond = and i1 %6, %7
  br i1 %or.cond, label %8, label %10

8:                                                ; preds = %5, %2
  %9 = sext i8 %0 to i32
  br label %13

10:                                               ; preds = %5
  %11 = sext i8 %0 to i32
  %12 = sdiv i32 %11, %3
  br label %13

13:                                               ; preds = %10, %8
  %14 = phi i32 [ %9, %8 ], [ %12, %10 ]
  %15 = trunc i32 %14 to i8
  ret i8 %15
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i8* @func_39(i64 %0, i8** %1, i8* %2) unnamed_addr #0 {
  %.sroa.0 = alloca i8*
  br label %4

4:                                                ; preds = %6, %3
  %storemerge = phi i32 [ 0, %3 ], [ %7, %6 ]
  %5 = icmp ult i32 %storemerge, 2
  br i1 %5, label %6, label %8

6:                                                ; preds = %4
  %7 = add nuw nsw i32 %storemerge, 1
  br label %4

8:                                                ; preds = %4
  %9 = load i32, i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 7), align 4, !tbaa !6
  %10 = or i32 %9, -472615634
  store i32 %10, i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 7), align 4, !tbaa !6
  %11 = trunc i64 %0 to i16
  store i16 %11, i16* @g_58, align 2, !tbaa !9
  %12 = call fastcc zeroext i16 @safe_add_func_uint16_t_u_u(i16 zeroext %11, i16 zeroext 27281)
  %13 = call fastcc zeroext i16 @safe_sub_func_uint16_t_u_u(i16 zeroext %12, i16 zeroext 16899)
  %14 = load i8, i8* @g_20, align 1, !tbaa !8
  %15 = sext i8 %14 to i32
  %16 = call fastcc signext i16 @safe_rshift_func_int16_t_s_s(i16 signext %13, i32 %15)
  %17 = trunc i64 %0 to i8
  %18 = trunc i64 %0 to i32
  %19 = call fastcc i8** @func_67(i16* nonnull @g_58, i16 signext %16, i8 zeroext %17, i8* null, i32 %18)
  %20 = icmp ne i64 %0, 1
  %21 = zext i1 %20 to i32
  %22 = load i32, i32* @g_142, align 4, !tbaa !6
  %23 = and i32 %22, %21
  %24 = trunc i32 %23 to i16
  %25 = load i32, i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 7), align 4, !tbaa !6
  %26 = sext i32 %25 to i64
  %27 = call fastcc zeroext i16 @func_59(i16 zeroext %24, i64 %26, i8 zeroext %17, i8 zeroext %17, i8* null)
  %28 = call fastcc signext i16 @safe_div_func_int16_t_s_s(i16 signext %11, i16 signext %27)
  %29 = trunc i16 %28 to i8
  %30 = call fastcc signext i8 @safe_lshift_func_int8_t_s_u(i8 signext %29, i32 %18)
  %31 = sext i8 %30 to i32
  store i32 %31, i32* @g_171, align 4, !tbaa !6
  %32 = load i32, i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 7), align 4, !tbaa !6
  %33 = trunc i32 %32 to i8
  %34 = call fastcc signext i8 @safe_lshift_func_int8_t_s_s(i8 signext %33, i32 1)
  %35 = icmp eq i8 %34, 0
  br i1 %35, label %39, label %36

36:                                               ; preds = %8
  %37 = load i32, i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 7), align 4, !tbaa !6
  %38 = icmp ne i32 %37, 0
  %phitmp1 = zext i1 %38 to i64
  br label %39

39:                                               ; preds = %36, %8
  %40 = phi i64 [ 0, %8 ], [ %phitmp1, %36 ]
  %41 = call fastcc i64 @safe_mod_func_int64_t_s_s(i64 0, i64 %40)
  %42 = trunc i64 %41 to i32
  store i32 %42, i32* @g_172, align 4, !tbaa !6
  %43 = call fastcc i64 @safe_unary_minus_func_uint64_t_u(i64 1)
  store i32 %18, i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 7), align 4, !tbaa !6
  %.sroa.0.0.copyload = load volatile i8*, i8** getelementptr inbounds (%union.U0, %union.U0* @g_106, i64 0, i32 0), align 8, !tbaa.struct !11
  store volatile i8* %.sroa.0.0.copyload, i8** %.sroa.0, !tbaa.struct !11
  %.sroa.0.0..sroa.0.0..sroa.0.0. = load i8*, i8** %.sroa.0
  ret i8* %.sroa.0.0..sroa.0.0..sroa.0.0.
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_lshift_func_int8_t_s_u(i8 signext %0, i32 %1) unnamed_addr #0 {
  %3 = sext i8 %0 to i32
  %4 = icmp slt i8 %0, 0
  %5 = icmp ugt i32 %1, 31
  %or.cond = or i1 %4, %5
  %6 = lshr i32 127, %1
  %7 = icmp slt i32 %6, %3
  %or.cond2 = or i1 %or.cond, %7
  %8 = select i1 %or.cond2, i32 0, i32 %1
  %9 = shl i32 %3, %8
  %10 = trunc i32 %9 to i8
  ret i8 %10
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i64 @safe_sub_func_int64_t_s_s(i64 %0, i64 %1) unnamed_addr #0 {
  %3 = xor i64 %0, %1
  %4 = and i64 %3, -9223372036854775808
  %5 = xor i64 %4, %0
  %6 = sub nsw i64 %5, %1
  %7 = xor i64 %6, %1
  %8 = and i64 %3, %7
  %9 = icmp slt i64 %8, 0
  %10 = select i1 %9, i64 0, i64 %1
  %11 = sub nsw i64 %0, %10
  ret i64 %11
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i64 @safe_mod_func_int64_t_s_s(i64 %0, i64 %1) unnamed_addr #0 {
  br label %4

3:                                                ; No predecessors!
  br label %5

4:                                                ; preds = %2
  br label %6

5:                                                ; preds = %3
  br label %6

6:                                                ; preds = %5, %4
  ret i64 0
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i16 @safe_sub_func_uint16_t_u_u(i16 zeroext %0, i16 zeroext %1) unnamed_addr #0 {
  %3 = sub i16 %0, %1
  ret i16 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i16 @func_59(i16 zeroext %0, i64 %1, i8 zeroext %2, i8 zeroext %3, i8* %4) unnamed_addr #0 {
  %6 = call fastcc zeroext i8 @safe_sub_func_uint8_t_u_u(i8 zeroext 2, i8 zeroext 1)
  %7 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 0, i64 0, i64 1), align 4, !tbaa !6
  %8 = trunc i32 %7 to i8
  %9 = trunc i32 %7 to i16
  %10 = call fastcc signext i16 @safe_lshift_func_int16_t_s_s(i16 signext %9, i32 8)
  %11 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 0, i64 0, i64 1), align 4, !tbaa !6
  %12 = trunc i16 %0 to i8
  store i8 %12, i8* @g_111, align 1, !tbaa !8
  %13 = trunc i32 %11 to i16
  %14 = call fastcc signext i16 @safe_mul_func_int16_t_s_s(i16 signext 1, i16 signext %13)
  %.lobit = lshr i16 %14, 15
  %15 = trunc i16 %.lobit to i8
  %16 = call fastcc zeroext i8 @safe_add_func_uint8_t_u_u(i8 zeroext %12, i8 zeroext %15)
  %17 = zext i8 %16 to i32
  %18 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 0, i64 0, i64 1), align 4, !tbaa !6
  %19 = icmp sgt i32 %18, %17
  %20 = zext i1 %19 to i16
  %21 = call fastcc zeroext i16 @safe_mul_func_uint16_t_u_u(i16 zeroext %20, i16 zeroext %0)
  %22 = trunc i16 %21 to i8
  %23 = load i8, i8* @g_20, align 1, !tbaa !8
  %24 = and i8 %23, %22
  store i8 %24, i8* @g_20, align 1, !tbaa !8
  %25 = sext i8 %24 to i32
  %26 = or i32 %11, %25
  %27 = trunc i32 %26 to i16
  %28 = call fastcc zeroext i16 @safe_sub_func_uint16_t_u_u(i16 zeroext %10, i16 zeroext %27)
  %29 = zext i16 %28 to i32
  %30 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 0, i64 0, i64 1), align 4, !tbaa !6
  %31 = or i32 %30, %29
  %32 = trunc i32 %31 to i8
  %33 = and i8 %32, -27
  %34 = call fastcc signext i8 @safe_lshift_func_int8_t_s_u(i8 signext %33, i32 52377)
  %35 = sext i8 %34 to i32
  %36 = call fastcc signext i8 @safe_lshift_func_int8_t_s_u(i8 signext %8, i32 %35)
  %37 = load volatile i32*, i32** @g_118, align 8, !tbaa !0
  %38 = load i8, i8* @g_111, align 1, !tbaa !8
  %39 = zext i8 %38 to i32
  %40 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 1, i64 0, i64 1), align 4, !tbaa !6
  %41 = icmp sle i32 %40, %39
  %42 = zext i1 %41 to i8
  %43 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 0, i64 0, i64 1), align 4, !tbaa !6
  %44 = call fastcc zeroext i8 @safe_rshift_func_uint8_t_u_u(i8 zeroext %42, i32 %43)
  %45 = load i64, i64* @g_11, align 8, !tbaa !4
  %46 = trunc i64 %45 to i32
  %47 = call fastcc signext i16 @safe_rshift_func_int16_t_s_u(i16 signext %0, i32 %46)
  %48 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 0, i64 0, i64 1), align 4, !tbaa !6
  %49 = icmp eq i32 %48, 1
  %50 = zext i1 %49 to i32
  %51 = load i32, i32* @g_142, align 4, !tbaa !6
  %52 = and i32 %51, %50
  store i32 %52, i32* @g_142, align 4, !tbaa !6
  ret i16 26043
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i8** @func_67(i16* %0, i16 signext %1, i8 zeroext %2, i8* %3, i32 %4) unnamed_addr #0 {
  %.sroa.0 = alloca [860 x i8], align 16
  %.sroa.4 = alloca [144 x i8], align 16
  %.sroa.0.0.sroa_idx = getelementptr inbounds [860 x i8], [860 x i8]* %.sroa.0, i64 0, i64 0
  call void @llvm.lifetime.start.p0i8(i64 860, i8* %.sroa.0.0.sroa_idx)
  %.sroa.4.0.sroa_idx = getelementptr inbounds [144 x i8], [144 x i8]* %.sroa.4, i64 0, i64 0
  call void @llvm.lifetime.start.p0i8(i64 144, i8* %.sroa.4.0.sroa_idx)
  %.sroa.0.0.sroa_idx2 = getelementptr inbounds [860 x i8], [860 x i8]* %.sroa.0, i64 0, i64 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %.sroa.0.0.sroa_idx2, i8* align 16 bitcast ([4 x [9 x [7 x i32]]]* @__const.func_67.l_117 to i8*), i64 860, i1 false)
  %.sroa.3.0.copyload = load i32, i32* getelementptr inbounds ([4 x [9 x [7 x i32]]], [4 x [9 x [7 x i32]]]* @__const.func_67.l_117, i64 0, i64 3, i64 3, i64 5), align 4
  %.sroa.4.0.sroa_idx5 = getelementptr inbounds [144 x i8], [144 x i8]* %.sroa.4, i64 0, i64 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %.sroa.4.0.sroa_idx5, i8* align 16 bitcast (i32* getelementptr inbounds ([4 x [9 x [7 x i32]]], [4 x [9 x [7 x i32]]]* @__const.func_67.l_117, i64 0, i64 3, i64 3, i64 6) to i8*), i64 144, i1 false)
  br label %6

6:                                                ; preds = %8, %5
  %storemerge = phi i32 [ 0, %5 ], [ %9, %8 ]
  %7 = icmp ult i32 %storemerge, 3
  br i1 %7, label %8, label %10

8:                                                ; preds = %6
  %9 = add nuw nsw i32 %storemerge, 1
  br label %6

10:                                               ; preds = %6
  br label %11

11:                                               ; preds = %10
  br label %12

12:                                               ; preds = %11
  store i32 -1835502843, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 1, i64 0, i64 0), align 4, !tbaa !6
  %13 = load i16, i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 1), align 2, !tbaa !9
  %14 = add i16 %13, -1
  store i16 %14, i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 1), align 2, !tbaa !9
  %15 = icmp eq i16 %13, 0
  br i1 %15, label %23, label %16

16:                                               ; preds = %12
  store i64 1, i64* getelementptr inbounds ([4 x i64], [4 x i64]* @g_131, i64 0, i64 2), align 16, !tbaa !4
  %17 = load i32, i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 8), align 16, !tbaa !6
  %18 = trunc i32 %17 to i8
  store i8 %18, i8* @g_111, align 1, !tbaa !8
  %19 = call fastcc zeroext i8 @safe_rshift_func_uint8_t_u_u(i8 zeroext %18, i32 2)
  %20 = zext i8 %19 to i32
  %21 = call fastcc signext i16 @safe_mod_func_int16_t_s_s(i16 signext 0, i16 signext -21917)
  %22 = call fastcc signext i8 @safe_mul_func_int8_t_s_s(i8 signext 114, i8 signext 0)
  br label %23

23:                                               ; preds = %16, %12
  %24 = call fastcc zeroext i16 @safe_sub_func_uint16_t_u_u(i16 zeroext 1, i16 zeroext 0)
  %.sroa.0.0.sroa_idx12 = getelementptr inbounds [860 x i8], [860 x i8]* %.sroa.0, i64 0, i64 0
  call void @llvm.lifetime.end.p0i8(i64 860, i8* %.sroa.0.0.sroa_idx12)
  %.sroa.4.0.sroa_idx11 = getelementptr inbounds [144 x i8], [144 x i8]* %.sroa.4, i64 0, i64 0
  call void @llvm.lifetime.end.p0i8(i64 144, i8* %.sroa.4.0.sroa_idx11)
  ret i8** undef
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i8 @safe_sub_func_uint8_t_u_u(i8 zeroext %0, i8 zeroext %1) unnamed_addr #0 {
  ret i8 undef
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i16 @safe_mod_func_uint16_t_u_u(i16 zeroext %0, i16 zeroext %1) unnamed_addr #0 {
  br label %3

3:                                                ; preds = %2
  %4 = urem i16 %0, 4
  br label %5

5:                                                ; preds = %3
  ret i16 %4
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc void @crc32_8bytes(i64 %0) unnamed_addr #0 {
  %2 = trunc i64 %0 to i8
  call fastcc void @crc32_byte(i8 zeroext %2)
  %3 = lshr i64 %0, 8
  %4 = trunc i64 %3 to i8
  call fastcc void @crc32_byte(i8 zeroext %4)
  %5 = lshr i64 %0, 16
  %6 = trunc i64 %5 to i8
  call fastcc void @crc32_byte(i8 zeroext %6)
  %7 = lshr i64 %0, 24
  %8 = trunc i64 %7 to i8
  call fastcc void @crc32_byte(i8 zeroext %8)
  %9 = lshr i64 %0, 32
  %10 = trunc i64 %9 to i8
  call fastcc void @crc32_byte(i8 zeroext %10)
  %11 = lshr i64 %0, 40
  %12 = trunc i64 %11 to i8
  call fastcc void @crc32_byte(i8 zeroext %12)
  %13 = lshr i64 %0, 48
  %14 = trunc i64 %13 to i8
  call fastcc void @crc32_byte(i8 zeroext %14)
  %15 = lshr i64 %0, 56
  %16 = trunc i64 %15 to i8
  call fastcc void @crc32_byte(i8 zeroext %16)
  ret void
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc void @crc32_byte(i8 zeroext %0) unnamed_addr #0 {
  %2 = load i32, i32* @crc32_context, align 4, !tbaa !6
  %3 = lshr i32 %2, 8
  %4 = zext i8 %0 to i32
  %.masked = and i32 %2, 255
  %5 = xor i32 %.masked, %4
  %6 = zext i32 %5 to i64
  %7 = getelementptr inbounds [256 x i32], [256 x i32]* @crc32_tab, i64 0, i64 %6
  %8 = load i32, i32* %7, align 4, !tbaa !6
  %9 = xor i32 %3, %8
  store i32 %9, i32* @crc32_context, align 4, !tbaa !6
  ret void
}

attributes #0 = { minsize nounwind optsize uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="none" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { argmemonly nounwind willreturn }
attributes #2 = { nounwind readonly "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="none" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="none" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { nounwind readonly }
attributes #5 = { nounwind }

!0 = !{!1, !1, i64 0}
!1 = !{!"any pointer", !2, i64 0}
!2 = !{!"omnipotent char", !3, i64 0}
!3 = !{!"Simple C/C++ TBAA"}
!4 = !{!5, !5, i64 0}
!5 = !{!"long", !2, i64 0}
!6 = !{!7, !7, i64 0}
!7 = !{!"int", !2, i64 0}
!8 = !{!2, !2, i64 0}
!9 = !{!10, !10, i64 0}
!10 = !{!"short", !2, i64 0}
!11 = !{i64 0, i64 8, !0, i64 0, i64 4, !6, i64 0, i64 4, !6}
