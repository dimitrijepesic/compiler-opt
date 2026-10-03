source_filename = "-"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%union.U0 = type { i8* }

@.str = private unnamed_addr constant [2 x i8] c"1\00", align 1
@g_11 = internal unnamed_addr global i64 2445994675441619566, align 8
@.str.1 = private unnamed_addr constant [5 x i8] c"g_11\00", align 1
@g_18 = internal global [9 x i32] [i32 -1, i32 -1, i32 -1, i32 -1, i32 -1, i32 -1, i32 -1, i32 -1, i32 -1], align 16
@.str.2 = private unnamed_addr constant [8 x i8] c"g_18[i]\00", align 1
@.str.3 = private unnamed_addr constant [14 x i8] c"index = [%d]\0A\00", align 1
@g_20 = internal global i8 -91, align 1
@.str.4 = private unnamed_addr constant [5 x i8] c"g_20\00", align 1
@g_58 = internal global i16 13271, align 2
@.str.5 = private unnamed_addr constant [5 x i8] c"g_58\00", align 1
@g_89 = internal unnamed_addr global [8 x [7 x i16]] [[7 x i16] [i16 -13159, i16 1, i16 -16212, i16 26043, i16 -1, i16 26043, i16 -16212], [7 x i16] [i16 6, i16 6, i16 -1, i16 -7, i16 -1, i16 10895, i16 1057], [7 x i16] [i16 -13159, i16 26043, i16 22709, i16 22709, i16 26043, i16 -13159, i16 -1], [7 x i16] [i16 1, i16 -1, i16 30330, i16 30910, i16 -1, i16 -1, i16 30910], [7 x i16] [i16 0, i16 -4, i16 0, i16 1, i16 -1, i16 7424, i16 -13159], [7 x i16] [i16 30330, i16 -1, i16 1057, i16 30330, i16 1057, i16 6, i16 -2933], [7 x i16] [i16 -29117, i16 22709, i16 0, i16 1, i16 1, i16 -13159, i16 1], [7 x i16] [i16 6, i16 10895, i16 10895, i16 6, i16 31434, i16 1, i16 30330]], align 16
@.str.6 = private unnamed_addr constant [11 x i8] c"g_89[i][j]\00", align 1
@.str.7 = private unnamed_addr constant [18 x i8] c"index = [%d][%d]\0A\00", align 1
@g_91 = internal global [8 x i16] [i16 2853, i16 2853, i16 2853, i16 2853, i16 2853, i16 2853, i16 2853, i16 2853], align 16
@.str.8 = private unnamed_addr constant [8 x i8] c"g_91[i]\00", align 1
@g_111 = internal unnamed_addr global i8 -46, align 1
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
@g_512 = internal unnamed_addr global i32 3, align 4
@.str.21 = private unnamed_addr constant [6 x i8] c"g_512\00", align 1
@.str.22 = private unnamed_addr constant [6 x i8] c"g_543\00", align 1
@g_575 = internal unnamed_addr global i64 -5213770106506113412, align 8
@.str.23 = private unnamed_addr constant [6 x i8] c"g_575\00", align 1
@crc32_context = internal unnamed_addr global i32 -1, align 4
@crc32_tab = internal unnamed_addr global [256 x i32] zeroinitializer, align 16
@g_642 = internal unnamed_addr global %union.U0* @g_640, align 8
@g_118 = internal global i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 1, i64 0, i64 0), align 8
@g_215 = internal unnamed_addr global i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 8), align 8
@g_432 = internal global i16* @g_58, align 8
@g_640 = internal global %union.U0 zeroinitializer, align 8
@__const.func_2.l_509 = private unnamed_addr constant [1 x [3 x [9 x i32]]] [[3 x [9 x i32]] [[9 x i32] [i32 9, i32 9, i32 9, i32 9, i32 9, i32 9, i32 9, i32 9, i32 9], [9 x i32] [i32 -1914901143, i32 -1914901143, i32 -1914901143, i32 -1914901143, i32 -1914901143, i32 -1914901143, i32 -1914901143, i32 -1914901143, i32 -1914901143], [9 x i32] [i32 9, i32 9, i32 9, i32 9, i32 9, i32 9, i32 9, i32 9, i32 9]]], align 16
@g_44 = internal global i8* @g_20, align 8
@g_543 = internal constant i8 -20, align 1
@g_427 = internal global i32* @g_171, align 8
@g_141 = internal global [6 x i32*] [i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*)], align 16
@g_635 = internal unnamed_addr global i8**** getelementptr inbounds ([5 x i8***], [5 x i8***]* @g_636, i64 0, i64 3), align 8
@g_636 = internal global [5 x i8***] [i8*** @g_637, i8*** @g_637, i8*** @g_637, i8*** @g_637, i8*** @g_637], align 16
@g_637 = internal global i8** getelementptr inbounds ([4 x [8 x [4 x i8*]]], [4 x [8 x [4 x i8*]]]* @g_638, i64 0, i64 3, i64 4, i64 0), align 8
@g_638 = internal global [4 x [8 x [4 x i8*]]] [[8 x [4 x i8*]] [[4 x i8*] [i8* @g_400, i8* @g_400, i8* null, i8* @g_400], [4 x i8*] [i8* @g_400, i8* @g_20, i8* @g_20, i8* @g_400], [4 x i8*] [i8* @g_20, i8* @g_320, i8* null, i8* @g_400], [4 x i8*] [i8* @g_20, i8* null, i8* @g_320, i8* @g_320], [4 x i8*] [i8* @g_20, i8* @g_400, i8* null, i8* @g_320], [4 x i8*] [i8* null, i8* null, i8* @g_20, i8* @g_400], [4 x i8*] [i8* @g_400, i8* @g_320, i8* @g_20, i8* @g_400], [4 x i8*] [i8* null, i8* @g_20, i8* @g_20, i8* @g_400]], [8 x [4 x i8*]] [[4 x i8*] [i8* null, i8* @g_400, i8* null, i8* @g_400], [4 x i8*] [i8* @g_20, i8* @g_20, i8* null, i8* null], [4 x i8*] [i8* @g_320, i8* @g_400, i8* null, i8* @g_400], [4 x i8*] [i8* @g_20, i8* @g_20, i8* @g_20, i8* @g_20], [4 x i8*] [i8* @g_320, i8* null, i8* @g_400, i8* null], [4 x i8*] [i8* null, i8* @g_20, i8* @g_20, i8* @g_400], [4 x i8*] [i8* null, i8* @g_400, i8* @g_400, i8* @g_400], [4 x i8*] [i8* @g_320, i8* @g_400, i8* @g_20, i8* @g_320]], [8 x [4 x i8*]] [[4 x i8*] [i8* @g_20, i8* @g_400, i8* null, i8* @g_320], [4 x i8*] [i8* @g_320, i8* @g_20, i8* null, i8* @g_20], [4 x i8*] [i8* @g_20, i8* @g_400, i8* null, i8* @g_400], [4 x i8*] [i8* null, i8* @g_20, i8* @g_20, i8* @g_20], [4 x i8*] [i8* null, i8* null, i8* @g_20, i8* @g_20], [4 x i8*] [i8* @g_400, i8* @g_320, i8* @g_20, i8* null], [4 x i8*] [i8* @g_320, i8* @g_400, i8* @g_20, i8* @g_20], [4 x i8*] [i8* @g_400, i8* @g_400, i8* null, i8* null]], [8 x [4 x i8*]] [[4 x i8*] [i8* @g_400, i8* @g_320, i8* @g_400, i8* @g_400], [4 x i8*] [i8* null, i8* null, i8* null, i8* @g_400], [4 x i8*] [i8* @g_20, i8* @g_20, i8* null, i8* @g_20], [4 x i8*] [i8* @g_400, i8* @g_400, i8* @g_20, i8* @g_400], [4 x i8*] [i8* null, i8* @g_20, i8* @g_320, i8* null], [4 x i8*] [i8* @g_20, i8* @g_20, i8* @g_20, i8* @g_20], [4 x i8*] [i8* @g_400, i8* @g_20, i8* @g_320, i8* @g_320], [4 x i8*] [i8* null, i8* @g_400, i8* null, i8* @g_20]]], align 16
@g_413 = internal global i32** @g_414, align 8
@g_106 = internal global %union.U0 zeroinitializer, align 8
@__const.func_59.l_169 = private unnamed_addr constant [2 x [10 x [5 x i32]]] [[10 x [5 x i32]] [[5 x i32] [i32 9, i32 355570572, i32 355570572, i32 9, i32 355570572], [5 x i32] [i32 9, i32 9, i32 -909000219, i32 9, i32 9], [5 x i32] [i32 355570572, i32 9, i32 355570572, i32 355570572, i32 9], [5 x i32] [i32 9, i32 355570572, i32 355570572, i32 9, i32 355570572], [5 x i32] [i32 9, i32 9, i32 -909000219, i32 9, i32 9], [5 x i32] [i32 355570572, i32 9, i32 355570572, i32 355570572, i32 9], [5 x i32] [i32 9, i32 355570572, i32 355570572, i32 9, i32 355570572], [5 x i32] [i32 9, i32 9, i32 -909000219, i32 9, i32 9], [5 x i32] [i32 355570572, i32 9, i32 355570572, i32 355570572, i32 355570572], [5 x i32] [i32 355570572, i32 -909000219, i32 -909000219, i32 355570572, i32 -909000219]], [10 x [5 x i32]] [[5 x i32] [i32 355570572, i32 355570572, i32 9, i32 355570572, i32 355570572], [5 x i32] [i32 -909000219, i32 355570572, i32 -909000219, i32 -909000219, i32 355570572], [5 x i32] [i32 355570572, i32 -909000219, i32 -909000219, i32 355570572, i32 -909000219], [5 x i32] [i32 355570572, i32 355570572, i32 9, i32 355570572, i32 355570572], [5 x i32] [i32 -909000219, i32 355570572, i32 -909000219, i32 -909000219, i32 355570572], [5 x i32] [i32 355570572, i32 -909000219, i32 -909000219, i32 355570572, i32 -909000219], [5 x i32] [i32 355570572, i32 355570572, i32 9, i32 355570572, i32 355570572], [5 x i32] [i32 -909000219, i32 355570572, i32 -909000219, i32 -909000219, i32 355570572], [5 x i32] [i32 355570572, i32 -909000219, i32 -909000219, i32 355570572, i32 -909000219], [5 x i32] [i32 355570572, i32 355570572, i32 9, i32 355570572, i32 355570572]]], align 16
@__const.func_67.l_117 = private unnamed_addr constant [4 x [9 x [7 x i32]]] [[9 x [7 x i32]] [[7 x i32] [i32 -1854576997, i32 -10, i32 -132096905, i32 3, i32 -8, i32 0, i32 616214352], [7 x i32] [i32 644334297, i32 -1, i32 395129846, i32 3, i32 1, i32 1, i32 -6], [7 x i32] [i32 -666901769, i32 -1, i32 0, i32 598164268, i32 1, i32 1002172723, i32 0], [7 x i32] [i32 -4, i32 0, i32 -529762007, i32 1371323651, i32 0, i32 -6, i32 0], [7 x i32] [i32 0, i32 -1, i32 8, i32 -6, i32 -2084893204, i32 0, i32 0], [7 x i32] [i32 1, i32 -1898913509, i32 0, i32 395129846, i32 -1959817787, i32 7, i32 -1959817787], [7 x i32] [i32 -2020256058, i32 9, i32 9, i32 -2020256058, i32 1, i32 -4, i32 2094105380], [7 x i32] [i32 1738015974, i32 1, i32 -3, i32 644334297, i32 1368777155, i32 -1857300812, i32 0], [7 x i32] [i32 196414362, i32 5, i32 1046977674, i32 -50136740, i32 0, i32 -6, i32 2094105380]], [9 x [7 x i32]] [[7 x i32] [i32 -1898913509, i32 7, i32 -4, i32 1195450976, i32 -6, i32 1, i32 -1959817787], [7 x i32] [i32 616214352, i32 0, i32 0, i32 -10, i32 8, i32 0, i32 0], [7 x i32] [i32 -3, i32 -1857300812, i32 -1, i32 -1, i32 -1777700, i32 1, i32 0], [7 x i32] [i32 2094105380, i32 1061555381, i32 -595724751, i32 8, i32 1000399752, i32 -6, i32 0], [7 x i32] [i32 -101267165, i32 -6, i32 -1, i32 -9, i32 -9, i32 -1, i32 -6], [7 x i32] [i32 -8, i32 638244229, i32 -6, i32 0, i32 0, i32 -132096905, i32 616214352], [7 x i32] [i32 0, i32 644334297, i32 -8, i32 -1, i32 -764956739, i32 1371323651, i32 1], [7 x i32] [i32 692398238, i32 2094105380, i32 -1, i32 0, i32 196414362, i32 -8, i32 -132096905], [7 x i32] [i32 2, i32 1, i32 524824689, i32 -9, i32 -1, i32 -1776562575, i32 -10]], [9 x [7 x i32]] [[7 x i32] [i32 9, i32 -2110602377, i32 1061555381, i32 8, i32 2, i32 1, i32 1002172723], [7 x i32] [i32 0, i32 4, i32 0, i32 -1, i32 1368777155, i32 1, i32 2], [7 x i32] [i32 0, i32 -1, i32 73832907, i32 8, i32 5, i32 -2, i32 -2], [7 x i32] [i32 0, i32 0, i32 395129846, i32 0, i32 0, i32 -1, i32 4], [7 x i32] [i32 -1, i32 0, i32 -1, i32 1002172723, i32 -2020256058, i32 1, i32 -6], [7 x i32] [i32 -1898913509, i32 1356777430, i32 1, i32 1738015974, i32 730521578, i32 -5, i32 -764956739], [7 x i32] [i32 -1, i32 1002172723, i32 -4, i32 -2, i32 692398238, i32 0, i32 1], [7 x i32] [i32 0, i32 -8, i32 1, i32 4, i32 -3, i32 -1857300812, i32 -1], [7 x i32] [i32 0, i32 1917141367, i32 196414362, i32 1061555381, i32 1002172723, i32 3, i32 0]], [9 x [7 x i32]] [[7 x i32] [i32 -9, i32 644334297, i32 524824689, i32 -1959817787, i32 1, i32 1, i32 4], [7 x i32] [i32 3, i32 0, i32 2094105380, i32 0, i32 -666901769, i32 0, i32 2094105380], [7 x i32] [i32 1914679593, i32 1914679593, i32 -1777700, i32 -4, i32 0, i32 1, i32 1356777430], [7 x i32] [i32 -1, i32 -5, i32 9, i32 0, i32 196414362, i32 -1, i32 0], [7 x i32] [i32 -1857300812, i32 0, i32 3, i32 -1776562575, i32 0, i32 -1719010738, i32 1738015974], [7 x i32] [i32 1936539133, i32 -8, i32 0, i32 355777422, i32 -666901769, i32 1002172723, i32 -1572771637], [7 x i32] [i32 -448216751, i32 -4, i32 -8, i32 -1, i32 1, i32 -1, i32 -3], [7 x i32] [i32 -1854576997, i32 -2, i32 -2084893204, i32 0, i32 1002172723, i32 -1, i32 -1], [7 x i32] [i32 1, i32 7, i32 1195450976, i32 730521578, i32 -3, i32 524824689, i32 841778661]]], align 16
@g_211 = internal global [7 x [2 x i32*]] [[2 x i32*] [i32* @g_171, i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*)], [2 x i32*] [i32* null, i32* @g_142], [2 x i32*] [i32* @g_142, i32* null], [2 x i32*] [i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* @g_171], [2 x i32*] [i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*), i32* null], [2 x i32*] [i32* @g_142, i32* @g_142], [2 x i32*] [i32* null, i32* bitcast (i8* getelementptr (i8, i8* bitcast ([9 x i32]* @g_18 to i8*), i64 32) to i32*)]], align 16
@g_240 = internal global i8* null, align 8
@g_414 = internal global i32* null, align 8
@.str.24 = private unnamed_addr constant [36 x i8] c"...checksum after hashing %s : %lX\0A\00", align 1
@.str.25 = private unnamed_addr constant [15 x i8] c"checksum = %X\0A\00", align 1

; Function Attrs: minsize nounwind optsize uwtable
define dso_local i32 @main(i32 %0, i8** %1) local_unnamed_addr #0 {
  %3 = icmp eq i32 %0, 2
  br i1 %3, label %4, label %9

4:                                                ; preds = %2
  %5 = getelementptr inbounds i8*, i8** %1, i64 1
  %6 = load i8*, i8** %5, align 8, !tbaa !0
  %7 = call i32 @strcmp(i8* nonnull dereferenceable(1) %6, i8* nonnull dereferenceable(2) getelementptr inbounds ([2 x i8], [2 x i8]* @.str, i64 0, i64 0)) #4
  %8 = icmp eq i32 %7, 0
  %spec.select = select i1 %8, i1 false, i1 true
  %spec.select10 = select i1 %8, i1 false, i1 true
  %spec.select11 = select i1 %8, i1 false, i1 true
  %spec.select12 = select i1 %8, i1 false, i1 true
  %spec.select13 = select i1 %8, i1 false, i1 true
  %spec.select14 = select i1 %8, i32 1, i32 0
  br label %9

9:                                                ; preds = %4, %2
  %phiofops9 = phi i1 [ true, %2 ], [ %spec.select, %4 ]
  %phiofops8 = phi i1 [ true, %2 ], [ %spec.select10, %4 ]
  %phiofops7 = phi i1 [ true, %2 ], [ %spec.select11, %4 ]
  %phiofops6 = phi i1 [ true, %2 ], [ %spec.select12, %4 ]
  %phiofops5 = phi i1 [ true, %2 ], [ %spec.select13, %4 ]
  %.0 = phi i32 [ 0, %2 ], [ %spec.select14, %4 ]
  call fastcc void @platform_main_begin()
  call fastcc void @crc32_gentab()
  %10 = call fastcc signext i16 @func_1()
  %11 = load i64, i64* @g_11, align 8, !tbaa !4
  call fastcc void @transparent_crc(i64 %11, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.1, i64 0, i64 0), i32 %.0)
  br label %12

12:                                               ; preds = %21, %9
  %.03 = phi i32 [ 0, %9 ], [ %22, %21 ]
  %13 = icmp ult i32 %.03, 9
  br i1 %13, label %14, label %23

14:                                               ; preds = %12
  %15 = zext i32 %.03 to i64
  %16 = getelementptr inbounds [9 x i32], [9 x i32]* @g_18, i64 0, i64 %15
  %17 = load i32, i32* %16, align 4, !tbaa !6
  %18 = sext i32 %17 to i64
  call fastcc void @transparent_crc(i64 %18, i8* getelementptr inbounds ([8 x i8], [8 x i8]* @.str.2, i64 0, i64 0), i32 %.0)
  br i1 %phiofops5, label %21, label %19

19:                                               ; preds = %14
  %20 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([14 x i8], [14 x i8]* @.str.3, i64 0, i64 0), i32 %.03) #5
  br label %21

21:                                               ; preds = %19, %14
  %22 = add nuw nsw i32 %.03, 1
  br label %12

23:                                               ; preds = %12
  %24 = load i8, i8* @g_20, align 1, !tbaa !8
  %25 = sext i8 %24 to i64
  call fastcc void @transparent_crc(i64 %25, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.4, i64 0, i64 0), i32 %.0)
  %26 = load i16, i16* @g_58, align 2, !tbaa !9
  %27 = sext i16 %26 to i64
  call fastcc void @transparent_crc(i64 %27, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.5, i64 0, i64 0), i32 %.0)
  br label %28

28:                                               ; preds = %42, %23
  %.14 = phi i32 [ 0, %23 ], [ %43, %42 ]
  %29 = icmp ult i32 %.14, 8
  br i1 %29, label %30, label %44

30:                                               ; preds = %40, %28
  %.02 = phi i32 [ %41, %40 ], [ 0, %28 ]
  %31 = icmp ult i32 %.02, 7
  br i1 %31, label %32, label %42

32:                                               ; preds = %30
  %33 = zext i32 %.14 to i64
  %34 = zext i32 %.02 to i64
  %35 = getelementptr inbounds [8 x [7 x i16]], [8 x [7 x i16]]* @g_89, i64 0, i64 %33, i64 %34
  %36 = load i16, i16* %35, align 2, !tbaa !9
  %37 = zext i16 %36 to i64
  call fastcc void @transparent_crc(i64 %37, i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.6, i64 0, i64 0), i32 %.0)
  br i1 %phiofops6, label %40, label %38

38:                                               ; preds = %32
  %39 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([18 x i8], [18 x i8]* @.str.7, i64 0, i64 0), i32 %.14, i32 %.02) #5
  br label %40

40:                                               ; preds = %38, %32
  %41 = add nuw nsw i32 %.02, 1
  br label %30

42:                                               ; preds = %30
  %43 = add nuw nsw i32 %.14, 1
  br label %28

44:                                               ; preds = %53, %28
  %.2 = phi i32 [ %54, %53 ], [ 0, %28 ]
  %45 = icmp ult i32 %.2, 8
  br i1 %45, label %46, label %55

46:                                               ; preds = %44
  %47 = zext i32 %.2 to i64
  %48 = getelementptr inbounds [8 x i16], [8 x i16]* @g_91, i64 0, i64 %47
  %49 = load i16, i16* %48, align 2, !tbaa !9
  %50 = zext i16 %49 to i64
  call fastcc void @transparent_crc(i64 %50, i8* getelementptr inbounds ([8 x i8], [8 x i8]* @.str.8, i64 0, i64 0), i32 %.0)
  br i1 %phiofops7, label %53, label %51

51:                                               ; preds = %46
  %52 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([14 x i8], [14 x i8]* @.str.3, i64 0, i64 0), i32 %.2) #5
  br label %53

53:                                               ; preds = %51, %46
  %54 = add nuw nsw i32 %.2, 1
  br label %44

55:                                               ; preds = %44
  %56 = load i8, i8* @g_111, align 1, !tbaa !8
  %57 = zext i8 %56 to i64
  call fastcc void @transparent_crc(i64 %57, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.9, i64 0, i64 0), i32 %.0)
  br label %58

58:                                               ; preds = %.critedge, %55
  %.3 = phi i32 [ 0, %55 ], [ %72, %.critedge ]
  %59 = icmp ult i32 %.3, 2
  br i1 %59, label %60, label %73

60:                                               ; preds = %70, %58
  %.01 = phi i32 [ %71, %70 ], [ 0, %58 ]
  %61 = icmp ult i32 %.01, 7
  br i1 %61, label %62, label %.critedge

62:                                               ; preds = %60
  %63 = zext i32 %.3 to i64
  %64 = zext i32 %.01 to i64
  %65 = getelementptr inbounds [2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 %63, i64 0, i64 %64
  %66 = load i32, i32* %65, align 4, !tbaa !6
  %67 = sext i32 %66 to i64
  call fastcc void @transparent_crc(i64 %67, i8* getelementptr inbounds ([15 x i8], [15 x i8]* @.str.10, i64 0, i64 0), i32 %.0)
  br i1 %phiofops8, label %70, label %68

68:                                               ; preds = %62
  %69 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([22 x i8], [22 x i8]* @.str.11, i64 0, i64 0), i32 %.3, i32 0, i32 %.01) #5
  br label %70

70:                                               ; preds = %68, %62
  %71 = add nuw nsw i32 %.01, 1
  br label %60

.critedge:                                        ; preds = %60
  %72 = add nuw nsw i32 %.3, 1
  br label %58

73:                                               ; preds = %81, %58
  %.4 = phi i32 [ %82, %81 ], [ 0, %58 ]
  %74 = icmp ult i32 %.4, 4
  br i1 %74, label %75, label %83

75:                                               ; preds = %73
  %76 = zext i32 %.4 to i64
  %77 = getelementptr inbounds [4 x i64], [4 x i64]* @g_131, i64 0, i64 %76
  %78 = load i64, i64* %77, align 8, !tbaa !4
  call fastcc void @transparent_crc(i64 %78, i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.str.12, i64 0, i64 0), i32 %.0)
  br i1 %phiofops9, label %81, label %79

79:                                               ; preds = %75
  %80 = call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([14 x i8], [14 x i8]* @.str.3, i64 0, i64 0), i32 %.4) #5
  br label %81

81:                                               ; preds = %79, %75
  %82 = add nuw nsw i32 %.4, 1
  br label %73

83:                                               ; preds = %73
  %84 = load i16, i16* @g_140, align 2, !tbaa !9
  %85 = sext i16 %84 to i64
  call fastcc void @transparent_crc(i64 %85, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.13, i64 0, i64 0), i32 %.0)
  %86 = load i32, i32* @g_142, align 4, !tbaa !6
  %87 = sext i32 %86 to i64
  call fastcc void @transparent_crc(i64 %87, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.14, i64 0, i64 0), i32 %.0)
  %88 = load i32, i32* @g_171, align 4, !tbaa !6
  %89 = sext i32 %88 to i64
  call fastcc void @transparent_crc(i64 %89, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.15, i64 0, i64 0), i32 %.0)
  %90 = load i32, i32* @g_172, align 4, !tbaa !6
  %91 = zext i32 %90 to i64
  call fastcc void @transparent_crc(i64 %91, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.16, i64 0, i64 0), i32 %.0)
  %92 = load i8, i8* @g_320, align 1, !tbaa !8
  %93 = sext i8 %92 to i64
  call fastcc void @transparent_crc(i64 %93, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.17, i64 0, i64 0), i32 %.0)
  %94 = load volatile i32, i32* @g_368, align 4, !tbaa !6
  %95 = sext i32 %94 to i64
  call fastcc void @transparent_crc(i64 %95, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.18, i64 0, i64 0), i32 %.0)
  %96 = load i16, i16* @g_397, align 2, !tbaa !9
  %97 = sext i16 %96 to i64
  call fastcc void @transparent_crc(i64 %97, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.19, i64 0, i64 0), i32 %.0)
  %98 = load i8, i8* @g_400, align 1, !tbaa !8
  %99 = sext i8 %98 to i64
  call fastcc void @transparent_crc(i64 %99, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.20, i64 0, i64 0), i32 %.0)
  %100 = load i32, i32* @g_512, align 4, !tbaa !6
  %101 = zext i32 %100 to i64
  call fastcc void @transparent_crc(i64 %101, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.21, i64 0, i64 0), i32 %.0)
  call fastcc void @transparent_crc(i64 236, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.22, i64 0, i64 0), i32 %.0)
  %102 = load i64, i64* @g_575, align 8, !tbaa !4
  call fastcc void @transparent_crc(i64 %102, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.23, i64 0, i64 0), i32 %.0)
  %103 = load i32, i32* @crc32_context, align 4, !tbaa !6
  %104 = xor i32 %103, -1
  call fastcc void @platform_main_end(i32 %104, i32 %.0)
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

1:                                                ; preds = %11, %0
  %.02 = phi i32 [ 0, %0 ], [ %14, %11 ]
  %2 = icmp ult i32 %.02, 256
  br i1 %2, label %3, label %15

3:                                                ; preds = %5, %1
  %.01 = phi i32 [ %10, %5 ], [ 8, %1 ]
  %.0 = phi i32 [ %.1, %5 ], [ %.02, %1 ]
  %4 = icmp sgt i32 %.01, 0
  br i1 %4, label %5, label %11

5:                                                ; preds = %3
  %6 = and i32 %.0, 1
  %7 = icmp eq i32 %6, 0
  %8 = lshr i32 %.0, 1
  %9 = xor i32 %8, -306674912
  %.1 = select i1 %7, i32 %8, i32 %9
  %10 = add nsw i32 %.01, -1
  br label %3

11:                                               ; preds = %3
  %12 = zext i32 %.02 to i64
  %13 = getelementptr inbounds [256 x i32], [256 x i32]* @crc32_tab, i64 0, i64 %12
  store i32 %.0, i32* %13, align 4, !tbaa !6
  %14 = add nuw nsw i32 %.02, 1
  br label %1

15:                                               ; preds = %1
  ret void
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @func_1() unnamed_addr #0 {
  %1 = call fastcc i8* @func_5(i32 -9, i32 -9)
  %2 = call fastcc %union.U0* @func_2(i8* %1, i16 signext -9)
  store %union.U0* %2, %union.U0** @g_642, align 8, !tbaa !0
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
  %.sroa.08 = alloca [7 x i32], align 16
  %.sroa.5 = alloca [28 x i8], align 16
  %.sroa.6 = alloca [44 x i8], align 16
  br label %6

6:                                                ; preds = %220, %2
  %storemerge = phi i16 [ 0, %2 ], [ %224, %220 ]
  store i16 %storemerge, i16* @g_397, align 2, !tbaa !9
  %7 = icmp slt i16 %storemerge, 15
  br i1 %7, label %8, label %225

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
  br label %12

12:                                               ; preds = %180, %8
  %storemerge4 = phi i64 [ 0, %8 ], [ %219, %180 ]
  %.01 = phi i32 [ -326220382, %8 ], [ %.1, %180 ]
  store i64 %storemerge4, i64* @g_11, align 8, !tbaa !4
  %13 = icmp eq i64 %storemerge4, 33
  br i1 %13, label %220, label %14

14:                                               ; preds = %12
  %.sroa.08.0.sroa_cast22 = bitcast [7 x i32]* %.sroa.08 to i8*
  call void @llvm.lifetime.start.p0i8(i64 28, i8* %.sroa.08.0.sroa_cast22)
  %.sroa.5.0.sroa_idx20 = getelementptr inbounds [28 x i8], [28 x i8]* %.sroa.5, i64 0, i64 0
  call void @llvm.lifetime.start.p0i8(i64 28, i8* %.sroa.5.0.sroa_idx20)
  %.sroa.6.0.sroa_idx18 = getelementptr inbounds [44 x i8], [44 x i8]* %.sroa.6, i64 0, i64 0
  call void @llvm.lifetime.start.p0i8(i64 44, i8* %.sroa.6.0.sroa_idx18)
  %.sroa.08.0.sroa_cast9 = bitcast [7 x i32]* %.sroa.08 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %.sroa.08.0.sroa_cast9, i8* align 16 bitcast ([1 x [3 x [9 x i32]]]* @__const.func_2.l_509 to i8*), i64 28, i1 false)
  %.sroa.5.0.sroa_idx12 = getelementptr inbounds [28 x i8], [28 x i8]* %.sroa.5, i64 0, i64 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %.sroa.5.0.sroa_idx12, i8* align 16 bitcast (i32* getelementptr inbounds ([1 x [3 x [9 x i32]]], [1 x [3 x [9 x i32]]]* @__const.func_2.l_509, i64 0, i64 0, i64 0, i64 8) to i8*), i64 28, i1 false)
  %.sroa.6.0.sroa_idx16 = getelementptr inbounds [44 x i8], [44 x i8]* %.sroa.6, i64 0, i64 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %.sroa.6.0.sroa_idx16, i8* align 16 bitcast (i32* getelementptr inbounds ([1 x [3 x [9 x i32]]], [1 x [3 x [9 x i32]]]* @__const.func_2.l_509, i64 0, i64 0, i64 1, i64 7) to i8*), i64 44, i1 false)
  br label %15

15:                                               ; preds = %17, %14
  %.0 = phi i32 [ 0, %14 ], [ %18, %17 ]
  %16 = icmp ult i32 %.0, 3
  br i1 %16, label %17, label %19

17:                                               ; preds = %15
  %18 = add nuw nsw i32 %.0, 1
  br label %15

19:                                               ; preds = %15
  %20 = sext i16 %1 to i32
  %21 = load i8*, i8** @g_44, align 8, !tbaa !0
  %22 = load i8, i8* %21, align 1, !tbaa !8
  %23 = call fastcc i32* @func_34(i32 %20, i8* null, i16 zeroext 19979, i8 signext %22)
  %24 = load i32, i32* %3, align 4, !tbaa !6
  %25 = load i32, i32* %23, align 4, !tbaa !6
  %26 = icmp eq i32 %25, 1
  %27 = call fastcc signext i8 @safe_rshift_func_int8_t_s_s(i8 signext 1, i32 %24)
  %28 = icmp eq i8 %27, 0
  %29 = and i1 %26, %28
  %30 = zext i1 %29 to i32
  %31 = and i32 %30, -1914901143
  store i8 0, i8* @g_111, align 1, !tbaa !8
  %32 = call fastcc zeroext i8 @safe_rshift_func_uint8_t_u_s(i8 zeroext 0, i32 6)
  %33 = load i32, i32* %23, align 4, !tbaa !6
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

46:                                               ; preds = %19
  %47 = load volatile i32, i32* @g_368, align 4, !tbaa !6
  %48 = load i8, i8* %0, align 1, !tbaa !8
  %49 = load i32, i32* %23, align 4, !tbaa !6
  %50 = trunc i32 %49 to i8
  store i8 %50, i8* @g_400, align 1, !tbaa !8
  %51 = load i32, i32* @g_512, align 4, !tbaa !6
  %52 = icmp ult i32 %31, %51
  %53 = zext i1 %52 to i32
  %54 = call fastcc i32 @safe_mod_func_uint32_t_u_u(i32 %53, i32 0)
  %55 = call fastcc signext i16 @safe_mul_func_int16_t_s_s(i16 signext 0, i16 signext %1)
  %56 = load volatile i32, i32* @g_368, align 4, !tbaa !6
  %57 = load i8*, i8** @g_44, align 8, !tbaa !0
  %58 = load i8, i8* %57, align 1, !tbaa !8
  %59 = sext i8 %58 to i32
  %60 = call fastcc signext i8 @safe_lshift_func_int8_t_s_s(i8 signext 0, i32 %59)
  %61 = sext i8 %60 to i32
  %62 = load i32, i32* @g_512, align 4, !tbaa !6
  %63 = xor i32 %62, %61
  %64 = icmp ne i32 %63, %20
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
  %74 = load i32, i32* %23, align 4, !tbaa !6
  %75 = trunc i32 %74 to i8
  %76 = call fastcc signext i8 @safe_add_func_int8_t_s_s(i8 signext %73, i8 signext %75)
  %77 = call fastcc signext i8 @safe_mod_func_int8_t_s_s(i8 signext %48, i8 signext %76)
  %78 = sext i8 %77 to i16
  %79 = call fastcc signext i16 @safe_div_func_int16_t_s_s(i16 signext 7, i16 signext %78)
  %80 = sext i16 %79 to i32
  %81 = or i32 %80, -1640375478
  %82 = and i32 %81, %20
  %83 = load volatile i32*, i32** @g_427, align 8, !tbaa !0
  store i32 %82, i32* %83, align 4, !tbaa !6
  br label %180

84:                                               ; preds = %106, %19
  %storemerge5 = phi i32 [ %141, %106 ], [ 0, %19 ]
  store i32 %storemerge5, i32* @g_512, align 4, !tbaa !6
  %85 = icmp ult i32 %storemerge5, 55
  br i1 %85, label %86, label %142

86:                                               ; preds = %84
  store volatile i32* %3, i32** getelementptr inbounds ([6 x i32*], [6 x i32*]* @g_141, i64 0, i64 0), align 16, !tbaa !0
  %87 = load volatile i16*, i16** @g_432, align 8, !tbaa !0
  %88 = load i16, i16* %87, align 2, !tbaa !9
  %89 = call fastcc signext i16 @safe_div_func_int16_t_s_s(i16 signext -7316, i16 signext %88)
  %90 = call fastcc signext i16 @safe_div_func_int16_t_s_s(i16 signext -30891, i16 signext 0)
  %91 = and i16 %90, 229
  %92 = zext i16 %91 to i32
  %93 = load i8, i8* @g_400, align 1, !tbaa !8
  %94 = sext i8 %93 to i64
  %95 = call fastcc i64 @safe_unary_minus_func_uint64_t_u(i64 %94)
  %96 = trunc i64 %95 to i32
  %97 = load i32, i32* %23, align 4, !tbaa !6
  %98 = trunc i32 %97 to i16
  %99 = load i8*, i8** @g_44, align 8, !tbaa !0
  %100 = load i8, i8* %99, align 1, !tbaa !8
  %101 = call fastcc i32* @func_34(i32 %96, i8* null, i16 zeroext %98, i8 signext %100)
  %102 = icmp eq i32* %101, @g_172
  br i1 %102, label %106, label %103

103:                                              ; preds = %86
  %104 = load i32, i32* %23, align 4, !tbaa !6
  %105 = icmp ne i32 %104, 0
  br label %106

106:                                              ; preds = %103, %86
  %107 = phi i1 [ false, %86 ], [ %105, %103 ]
  %108 = zext i1 %107 to i32
  %109 = call fastcc i32 @safe_mod_func_uint32_t_u_u(i32 %92, i32 %108)
  %110 = call fastcc i32 @safe_add_func_uint32_t_u_u(i32 %109, i32 2)
  %111 = call fastcc signext i16 @safe_mul_func_int16_t_s_s(i16 signext 1, i16 signext %1)
  %112 = load i32*, i32** @g_215, align 8, !tbaa !0
  store i32 1, i32* %112, align 4, !tbaa !6
  %113 = load i32, i32* @g_512, align 4, !tbaa !6
  %114 = zext i32 %113 to i64
  %115 = load volatile i32*, i32** @g_118, align 8, !tbaa !0
  %116 = load i32, i32* %115, align 4, !tbaa !6
  %117 = load i32, i32* %101, align 4, !tbaa !6
  %118 = add i32 %117, 1
  store i32 %118, i32* %101, align 4, !tbaa !6
  %119 = trunc i16 %1 to i8
  %120 = call fastcc zeroext i8 @safe_mod_func_uint8_t_u_u(i8 zeroext %119, i8 zeroext 1)
  %121 = zext i8 %120 to i64
  store i64 %121, i64* @g_575, align 8, !tbaa !4
  %122 = icmp slt i32 %116, 1
  %123 = zext i1 %122 to i64
  %124 = sext i16 %1 to i64
  %125 = and i64 %123, %124
  %126 = load i64, i64* @g_11, align 8, !tbaa !4
  %127 = or i64 %126, %125
  %128 = icmp ugt i64 %127, %114
  %129 = zext i1 %128 to i8
  %130 = call fastcc signext i8 @safe_unary_minus_func_int8_t_s(i8 signext %129)
  %131 = sext i8 %130 to i16
  %132 = load i32, i32* @g_172, align 4, !tbaa !6
  %133 = icmp ugt i32 %132, -14818
  %134 = zext i1 %133 to i8
  %135 = call fastcc signext i8 @safe_unary_minus_func_int8_t_s(i8 signext %134)
  %136 = call fastcc i32 @safe_sub_func_uint32_t_u_u(i32 1, i32 %20)
  %137 = call fastcc signext i16 @safe_rshift_func_int16_t_s_u(i16 signext %131, i32 %136)
  store i32 %20, i32* %23, align 4, !tbaa !6
  %138 = load i32, i32* @g_512, align 4, !tbaa !6
  %139 = trunc i32 %138 to i8
  %140 = call fastcc zeroext i8 @safe_add_func_uint8_t_u_u(i8 zeroext %139, i8 zeroext 1)
  %141 = zext i8 %140 to i32
  br label %84

142:                                              ; preds = %84
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
  %154 = icmp eq i8* %0, @g_543
  %155 = zext i1 %154 to i8
  %156 = call fastcc zeroext i8 @safe_mul_func_uint8_t_u_u(i8 zeroext %153, i8 zeroext %155)
  %157 = call fastcc signext i16 @safe_lshift_func_int16_t_s_u(i16 signext 0, i32 15)
  %158 = trunc i16 %157 to i8
  %159 = load i32, i32* %23, align 4, !tbaa !6
  %160 = call fastcc zeroext i8 @safe_lshift_func_uint8_t_u_u(i8 zeroext %158, i32 %159)
  %161 = load i16, i16* getelementptr inbounds ([8 x [7 x i16]], [8 x [7 x i16]]* @g_89, i64 0, i64 0, i64 3), align 2, !tbaa !9
  %162 = icmp eq i16 %161, 0
  %163 = zext i1 %162 to i8
  %164 = call fastcc signext i8 @safe_sub_func_int8_t_s_s(i8 signext %163, i8 signext 0)
  %165 = call fastcc signext i16 @safe_lshift_func_int16_t_s_s(i16 signext 1, i32 13)
  %166 = sext i16 %165 to i64
  %167 = load i64, i64* @g_11, align 8, !tbaa !4
  %168 = or i64 %167, %166
  %169 = icmp ugt i64 %168, %151
  %170 = and i1 %148, %169
  %171 = zext i1 %170 to i32
  %172 = load i8, i8* @g_400, align 1, !tbaa !8
  %173 = sext i8 %172 to i32
  %174 = icmp sgt i32 %171, %173
  %175 = zext i1 %174 to i64
  %176 = load i8, i8* @g_20, align 1, !tbaa !8
  %177 = sext i8 %176 to i64
  %178 = call fastcc i64 @safe_mod_func_uint64_t_u_u(i64 %175, i64 %177)
  store i32 1, i32* %23, align 4, !tbaa !6
  %179 = or i32 %.01, 1
  br label %180

180:                                              ; preds = %142, %46
  %.1 = phi i32 [ %.01, %46 ], [ %179, %142 ]
  %181 = load i8*, i8** @g_44, align 8, !tbaa !0
  %182 = load i8, i8* %181, align 1, !tbaa !8
  %183 = load i64, i64* @g_575, align 8, !tbaa !4
  %184 = add i64 %183, -1
  store i64 %184, i64* @g_575, align 8, !tbaa !4
  %185 = load i64, i64* getelementptr inbounds ([4 x i64], [4 x i64]* @g_131, i64 0, i64 1), align 8, !tbaa !4
  store i64 %185, i64* getelementptr inbounds ([4 x i64], [4 x i64]* @g_131, i64 0, i64 3), align 8, !tbaa !4
  %186 = icmp ule i64 %184, %185
  %187 = zext i1 %186 to i16
  %188 = load i16, i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 4), align 8, !tbaa !9
  %189 = trunc i16 %188 to i8
  store i8 %189, i8* @g_111, align 1, !tbaa !8
  %190 = call fastcc zeroext i8 @safe_mod_func_uint8_t_u_u(i8 zeroext 0, i8 zeroext 8)
  %191 = zext i8 %190 to i32
  store i32 %191, i32* %23, align 4, !tbaa !6
  %192 = call fastcc zeroext i8 @safe_lshift_func_uint8_t_u_u(i8 zeroext 1, i32 %20)
  %193 = zext i8 %192 to i16
  %194 = or i16 %193, %1
  %195 = load i16, i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 7), align 2, !tbaa !9
  %196 = or i16 %194, %195
  %197 = call fastcc signext i16 @safe_sub_func_int16_t_s_s(i16 signext %187, i16 signext %196)
  %198 = call fastcc i64 @safe_div_func_int64_t_s_s(i64 1, i64 2)
  %199 = trunc i64 %198 to i16
  %200 = load volatile i16*, i16** @g_432, align 8, !tbaa !0
  %201 = load i16, i16* %200, align 2, !tbaa !9
  %202 = call fastcc zeroext i16 @safe_mul_func_uint16_t_u_u(i16 zeroext %199, i16 zeroext %201)
  %203 = zext i16 %202 to i32
  %204 = call fastcc i32 @safe_mod_func_int32_t_s_s(i32 %20, i32 %203)
  %205 = call fastcc i32 @safe_add_func_int32_t_s_s(i32 %204, i32 %.1)
  %206 = trunc i32 %205 to i8
  %207 = load i8*, i8** @g_44, align 8, !tbaa !0
  %208 = load i8, i8* %207, align 1, !tbaa !8
  %209 = sext i8 %208 to i32
  %210 = call fastcc signext i8 @safe_rshift_func_int8_t_s_s(i8 signext %206, i32 %209)
  %211 = load i8*, i8** @g_44, align 8, !tbaa !0
  %212 = load i8, i8* %211, align 1, !tbaa !8
  %213 = sext i8 %212 to i32
  %214 = call fastcc signext i8 @safe_rshift_func_int8_t_s_s(i8 signext %182, i32 %213)
  %215 = icmp eq i8 %214, 0
  %216 = zext i1 %215 to i32
  %217 = call fastcc i32 @safe_div_func_int32_t_s_s(i32 %216, i32 1)
  store i8**** %5, i8***** @g_635, align 8, !tbaa !0
  %.sroa.08.0.sroa_cast23 = bitcast [7 x i32]* %.sroa.08 to i8*
  call void @llvm.lifetime.end.p0i8(i64 28, i8* %.sroa.08.0.sroa_cast23)
  %.sroa.5.0.sroa_idx21 = getelementptr inbounds [28 x i8], [28 x i8]* %.sroa.5, i64 0, i64 0
  call void @llvm.lifetime.end.p0i8(i64 28, i8* %.sroa.5.0.sroa_idx21)
  %.sroa.6.0.sroa_idx19 = getelementptr inbounds [44 x i8], [44 x i8]* %.sroa.6, i64 0, i64 0
  call void @llvm.lifetime.end.p0i8(i64 44, i8* %.sroa.6.0.sroa_idx19)
  %218 = load i64, i64* @g_11, align 8, !tbaa !4
  %219 = add i64 %218, 1
  br label %12

220:                                              ; preds = %12
  call void @llvm.lifetime.end.p0i8(i64 8, i8* nonnull %11) #5
  call void @llvm.lifetime.end.p0i8(i64 8, i8* nonnull %10) #5
  call void @llvm.lifetime.end.p0i8(i64 4, i8* nonnull %9) #5
  %221 = load i16, i16* @g_397, align 2, !tbaa !9
  %222 = sext i16 %221 to i64
  %223 = call fastcc i64 @safe_add_func_int64_t_s_s(i64 %222, i64 2)
  %224 = trunc i64 %223 to i16
  br label %6

225:                                              ; preds = %6
  ret %union.U0* @g_640
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i8* @func_5(i32 %0, i32 %1) unnamed_addr #0 {
  br label %3

3:                                                ; preds = %5, %2
  %.02 = phi i32 [ 0, %2 ], [ %6, %5 ]
  %4 = icmp ult i32 %.02, 2
  br i1 %4, label %5, label %7

5:                                                ; preds = %3
  %6 = add nuw nsw i32 %.02, 1
  br label %3

7:                                                ; preds = %3
  %8 = load i32, i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 7), align 4, !tbaa !6
  %9 = call fastcc i32 @safe_sub_func_uint32_t_u_u(i32 -729453352, i32 %8)
  %10 = trunc i32 %9 to i8
  %11 = call fastcc i8* @func_30(i8 zeroext %10)
  %12 = icmp eq i8* %11, @g_20
  %13 = zext i1 %12 to i16
  %14 = trunc i32 %0 to i16
  %15 = call fastcc i8* @func_24(i16 signext %13, i16 zeroext %14, i32 27)
  %16 = call fastcc i32* @func_12(i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 8), i8* nonnull @g_20, i32* null, i8* %15)
  ret i8* @g_20
}

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
  store i8 68, i8* @g_111, align 1, !tbaa !8
  %8 = call fastcc zeroext i8 @safe_rshift_func_uint8_t_u_u(i8 zeroext 68, i32 6)
  %9 = call fastcc signext i16 @safe_mul_func_int16_t_s_s(i16 signext 1, i16 signext 3954)
  %10 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 1, i64 0, i64 0), align 4, !tbaa !6
  %11 = or i32 %10, -350089660
  store i32 %11, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 1, i64 0, i64 0), align 4, !tbaa !6
  ret i32* @g_142
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
  %5 = icmp slt i32 %1, 0
  %or.cond = or i1 %4, %5
  %6 = icmp sgt i32 %1, 31
  %or.cond2 = or i1 %6, %or.cond
  %7 = lshr i32 32767, %1
  %8 = icmp slt i32 %7, %3
  %or.cond4 = or i1 %8, %or.cond2
  %9 = shl i32 %3, %1
  %10 = select i1 %or.cond4, i32 %3, i32 %9
  %11 = trunc i32 %10 to i16
  ret i16 %11
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i32 @safe_add_func_int32_t_s_s(i32 %0, i32 %1) unnamed_addr #0 {
  %3 = icmp sgt i32 %0, 0
  br i1 %3, label %4, label %8

4:                                                ; preds = %2
  %5 = icmp sgt i32 %1, 0
  %6 = sub nuw nsw i32 2147483647, %1
  %7 = icmp slt i32 %6, %0
  %or.cond = and i1 %5, %7
  br i1 %or.cond, label %14, label %.thread

8:                                                ; preds = %2
  %9 = icmp slt i32 %0, 0
  %10 = icmp slt i32 %1, 0
  %or.cond3 = and i1 %9, %10
  %11 = sub nsw i32 -2147483648, %1
  %12 = icmp sgt i32 %11, %0
  %or.cond5 = and i1 %or.cond3, %12
  br i1 %or.cond5, label %14, label %.thread

.thread:                                          ; preds = %8, %4
  %13 = add nsw i32 %1, %0
  br label %14

14:                                               ; preds = %.thread, %8, %4
  %15 = phi i32 [ %13, %.thread ], [ %0, %4 ], [ %0, %8 ]
  ret i32 %15
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i8 @safe_rshift_func_uint8_t_u_s(i8 zeroext %0, i32 %1) unnamed_addr #0 {
  %3 = icmp slt i32 %1, 0
  %4 = icmp sgt i32 %1, 31
  %or.cond = or i1 %3, %4
  %5 = zext i8 %0 to i32
  %6 = zext i8 %0 to i32
  %7 = lshr i32 %6, %1
  %8 = select i1 %or.cond, i32 %5, i32 %7
  %9 = trunc i32 %8 to i8
  ret i8 %9
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_rshift_func_int8_t_s_s(i8 signext %0, i32 %1) unnamed_addr #0 {
  %3 = sext i8 %0 to i32
  %4 = icmp slt i8 %0, 0
  %5 = icmp slt i32 %1, 0
  %or.cond = or i1 %4, %5
  %6 = icmp sgt i32 %1, 31
  %or.cond1 = or i1 %6, %or.cond
  %7 = ashr i32 %3, %1
  %8 = select i1 %or.cond1, i32 %3, i32 %7
  %9 = trunc i32 %8 to i8
  ret i8 %9
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @safe_div_func_int16_t_s_s(i16 signext %0, i16 signext %1) unnamed_addr #0 {
  %3 = icmp eq i16 %1, 0
  br i1 %3, label %7, label %4

4:                                                ; preds = %2
  %5 = icmp eq i16 %0, -32768
  %6 = icmp eq i16 %1, -1
  %or.cond = and i1 %5, %6
  br i1 %or.cond, label %7, label %9

7:                                                ; preds = %4, %2
  %8 = sext i16 %0 to i32
  br label %13

9:                                                ; preds = %4
  %10 = sext i16 %0 to i32
  %11 = sext i16 %1 to i32
  %12 = sdiv i32 %10, %11
  br label %13

13:                                               ; preds = %9, %7
  %14 = phi i32 [ %8, %7 ], [ %12, %9 ]
  %15 = trunc i32 %14 to i16
  ret i16 %15
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_mod_func_int8_t_s_s(i8 signext %0, i8 signext %1) unnamed_addr #0 {
  %3 = icmp eq i8 %1, 0
  br i1 %3, label %7, label %4

4:                                                ; preds = %2
  %5 = icmp eq i8 %0, -128
  %6 = icmp eq i8 %1, -1
  %or.cond = and i1 %5, %6
  br i1 %or.cond, label %7, label %9

7:                                                ; preds = %4, %2
  %8 = sext i8 %0 to i32
  br label %13

9:                                                ; preds = %4
  %10 = sext i8 %0 to i32
  %11 = sext i8 %1 to i32
  %12 = srem i32 %10, %11
  br label %13

13:                                               ; preds = %9, %7
  %14 = phi i32 [ %8, %7 ], [ %12, %9 ]
  %15 = trunc i32 %14 to i8
  ret i8 %15
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_add_func_int8_t_s_s(i8 signext %0, i8 signext %1) unnamed_addr #0 {
  %3 = add i8 %1, %0
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
  %6 = ashr i32 %3, %1
  %7 = select i1 %or.cond, i32 %3, i32 %6
  %8 = trunc i32 %7 to i8
  ret i8 %8
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_lshift_func_int8_t_s_s(i8 signext %0, i32 %1) unnamed_addr #0 {
  %3 = sext i8 %0 to i32
  %4 = icmp slt i8 %0, 0
  %5 = icmp slt i32 %1, 0
  %or.cond = or i1 %4, %5
  %6 = icmp sgt i32 %1, 31
  %or.cond2 = or i1 %6, %or.cond
  %7 = lshr i32 127, %1
  %8 = icmp slt i32 %7, %3
  %or.cond4 = or i1 %8, %or.cond2
  %9 = shl i32 %3, %1
  %10 = select i1 %or.cond4, i32 %3, i32 %9
  %11 = trunc i32 %10 to i8
  ret i8 %11
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @safe_mul_func_int16_t_s_s(i16 signext %0, i16 signext %1) unnamed_addr #0 {
  %3 = mul i16 %1, %0
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
  %3 = add i32 %1, %0
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
  %6 = ashr i32 %3, %1
  %7 = select i1 %or.cond, i32 %3, i32 %6
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
  %3 = add i8 %1, %0
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
  %3 = mul i8 %1, %0
  ret i8 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i8 @safe_lshift_func_uint8_t_u_u(i8 zeroext %0, i32 %1) unnamed_addr #0 {
  %3 = icmp ugt i32 %1, 31
  br i1 %3, label %8, label %4

4:                                                ; preds = %2
  %5 = zext i8 %0 to i32
  %6 = lshr i32 255, %1
  %7 = icmp slt i32 %6, %5
  br i1 %7, label %8, label %10

8:                                                ; preds = %4, %2
  %9 = zext i8 %0 to i32
  br label %12

10:                                               ; preds = %4
  %11 = shl i32 %5, %1
  br label %12

12:                                               ; preds = %10, %8
  %13 = phi i32 [ %9, %8 ], [ %11, %10 ]
  %14 = trunc i32 %13 to i8
  ret i8 %14
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @safe_lshift_func_int16_t_s_u(i16 signext %0, i32 %1) unnamed_addr #0 {
  %3 = sext i16 %0 to i32
  %4 = icmp slt i16 %0, 0
  %5 = icmp ugt i32 %1, 31
  %or.cond = or i1 %4, %5
  %6 = lshr i32 32767, %1
  %7 = icmp slt i32 %6, %3
  %or.cond3 = or i1 %or.cond, %7
  %8 = shl i32 %3, %1
  %9 = select i1 %or.cond3, i32 %3, i32 %8
  %10 = trunc i32 %9 to i16
  ret i16 %10
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i32 @safe_div_func_int32_t_s_s(i32 %0, i32 %1) unnamed_addr #0 {
  %3 = icmp eq i32 %1, 0
  br i1 %3, label %9, label %4

4:                                                ; preds = %2
  %5 = icmp eq i32 %0, -2147483648
  %6 = icmp eq i32 %1, -1
  %or.cond = and i1 %5, %6
  br i1 %or.cond, label %9, label %7

7:                                                ; preds = %4
  %8 = sdiv i32 %0, %1
  br label %9

9:                                                ; preds = %7, %4, %2
  %10 = phi i32 [ %8, %7 ], [ %0, %2 ], [ -2147483648, %4 ]
  ret i32 %10
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i32 @safe_mod_func_int32_t_s_s(i32 %0, i32 %1) unnamed_addr #0 {
  %3 = icmp eq i32 %1, 0
  br i1 %3, label %9, label %4

4:                                                ; preds = %2
  %5 = icmp eq i32 %0, -2147483648
  %6 = icmp eq i32 %1, -1
  %or.cond = and i1 %5, %6
  br i1 %or.cond, label %9, label %7

7:                                                ; preds = %4
  %8 = srem i32 %0, %1
  br label %9

9:                                                ; preds = %7, %4, %2
  %10 = phi i32 [ %8, %7 ], [ %0, %2 ], [ -2147483648, %4 ]
  ret i32 %10
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i16 @safe_mul_func_uint16_t_u_u(i16 zeroext %0, i16 zeroext %1) unnamed_addr #0 {
  %3 = mul i16 %1, %0
  ret i16 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i64 @safe_div_func_int64_t_s_s(i64 %0, i64 %1) unnamed_addr #0 {
  %3 = icmp eq i64 %1, 0
  br i1 %3, label %9, label %4

4:                                                ; preds = %2
  %5 = icmp eq i64 %0, -9223372036854775808
  %6 = icmp eq i64 %1, -1
  %or.cond = and i1 %5, %6
  br i1 %or.cond, label %9, label %7

7:                                                ; preds = %4
  %8 = sdiv i64 %0, %1
  br label %9

9:                                                ; preds = %7, %4, %2
  %10 = phi i64 [ %8, %7 ], [ %0, %2 ], [ -9223372036854775808, %4 ]
  ret i64 %10
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i64 @safe_add_func_int64_t_s_s(i64 %0, i64 %1) unnamed_addr #0 {
  %3 = icmp sgt i64 %0, 0
  br i1 %3, label %4, label %8

4:                                                ; preds = %2
  %5 = icmp sgt i64 %1, 0
  %6 = sub nuw nsw i64 9223372036854775807, %1
  %7 = icmp slt i64 %6, %0
  %or.cond = and i1 %5, %7
  br i1 %or.cond, label %14, label %.thread

8:                                                ; preds = %2
  %9 = icmp slt i64 %0, 0
  %10 = icmp slt i64 %1, 0
  %or.cond3 = and i1 %9, %10
  %11 = sub nsw i64 -9223372036854775808, %1
  %12 = icmp sgt i64 %11, %0
  %or.cond5 = and i1 %or.cond3, %12
  br i1 %or.cond5, label %14, label %.thread

.thread:                                          ; preds = %8, %4
  %13 = add nsw i64 %1, %0
  br label %14

14:                                               ; preds = %.thread, %8, %4
  %15 = phi i64 [ %13, %.thread ], [ %0, %4 ], [ %0, %8 ]
  ret i64 %15
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i8 @safe_rshift_func_uint8_t_u_u(i8 zeroext %0, i32 %1) unnamed_addr #0 {
  %3 = icmp ugt i32 %1, 31
  %4 = zext i8 %0 to i32
  %5 = lshr i32 %4, %1
  %6 = select i1 %3, i32 %4, i32 %5
  %7 = trunc i32 %6 to i8
  ret i8 %7
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_mul_func_int8_t_s_s(i8 signext %0, i8 signext %1) unnamed_addr #0 {
  %3 = mul i8 %1, %0
  ret i8 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i32* @func_12(i32* %0, i8* %1, i32* %2, i8* %3) unnamed_addr #0 {
  %5 = alloca [2 x i32], align 4
  store i16 21, i16* @g_140, align 2, !tbaa !9
  %6 = bitcast [2 x i32]* %5 to i8*
  call void @llvm.lifetime.start.p0i8(i64 8, i8* nonnull %6) #5
  br label %7

7:                                                ; preds = %9, %4
  %.08 = phi i32 [ 0, %4 ], [ %12, %9 ]
  %8 = icmp ult i32 %.08, 2
  br i1 %8, label %9, label %13

9:                                                ; preds = %7
  %10 = zext i32 %.08 to i64
  %11 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 %10
  store i32 9, i32* %11, align 4, !tbaa !6
  %12 = add nuw nsw i32 %.08, 1
  br label %7

13:                                               ; preds = %7
  %14 = load i64, i64* @g_11, align 8, !tbaa !4
  %15 = add i64 %14, -1
  store i64 %15, i64* @g_11, align 8, !tbaa !4
  %16 = call fastcc i64 @safe_unary_minus_func_uint64_t_u(i64 %15)
  %17 = xor i64 %16, 3
  %18 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 1
  %19 = load i64, i64* getelementptr inbounds ([4 x i64], [4 x i64]* @g_131, i64 0, i64 1), align 8, !tbaa !4
  %20 = trunc i64 %19 to i16
  %21 = call fastcc signext i8 @safe_mul_func_int8_t_s_s(i8 signext 1, i8 signext 64)
  %22 = icmp eq i8 %21, 2
  %23 = zext i1 %22 to i8
  %24 = load i64, i64* getelementptr inbounds ([4 x i64], [4 x i64]* @g_131, i64 0, i64 2), align 16, !tbaa !4
  %25 = trunc i64 %24 to i8
  %26 = call fastcc signext i8 @safe_div_func_int8_t_s_s(i8 signext %23, i8 signext %25)
  %27 = sext i8 %26 to i32
  %28 = load i32, i32* @g_171, align 4, !tbaa !6
  %29 = call fastcc i32 @safe_div_func_uint32_t_u_u(i32 %27, i32 %28)
  %30 = load i8*, i8** @g_44, align 8, !tbaa !0
  %31 = load i8, i8* %30, align 1, !tbaa !8
  %32 = icmp eq i8 %31, 0
  %spec.select = select i1 %32, i32 0, i32 1
  %33 = getelementptr inbounds [2 x i32], [2 x i32]* %5, i64 0, i64 0
  %34 = load i32, i32* %33, align 4, !tbaa !6
  %35 = xor i32 %spec.select, %34
  %36 = call fastcc zeroext i16 @safe_rshift_func_uint16_t_u_u(i16 zeroext %20, i32 %35)
  %37 = zext i16 %36 to i64
  %38 = call fastcc i64 @safe_unary_minus_func_uint64_t_u(i64 %37)
  %39 = icmp eq i64 %38, 9
  %40 = zext i1 %39 to i64
  %41 = xor i64 %17, %40
  %42 = trunc i64 %41 to i8
  %43 = load i32, i32* %18, align 4, !tbaa !6
  %44 = trunc i32 %43 to i8
  %45 = call fastcc zeroext i8 @safe_mul_func_uint8_t_u_u(i8 zeroext %42, i8 zeroext %44)
  %46 = load i16, i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 6), align 4, !tbaa !9
  %47 = zext i16 %46 to i64
  %48 = trunc i32 %34 to i16
  %49 = call fastcc signext i16 @safe_mul_func_int16_t_s_s(i16 signext -18902, i16 signext %48)
  %50 = icmp ne i16 %49, 0
  %51 = zext i1 %50 to i16
  %52 = trunc i32 %43 to i16
  %53 = load i16, i16* getelementptr inbounds ([8 x [7 x i16]], [8 x [7 x i16]]* @g_89, i64 0, i64 1, i64 2), align 2, !tbaa !9
  %54 = zext i16 %53 to i32
  %55 = call fastcc i8* @func_24(i16 signext %51, i16 zeroext %52, i32 %54)
  %56 = call fastcc i8* @func_39(i64 %47, i8** nonnull @g_44, i8* %55)
  %57 = call fastcc i32 @safe_mod_func_uint32_t_u_u(i32 %43, i32 833339902)
  %58 = icmp eq i32 %57, 0
  %59 = load i8, i8* @g_20, align 1
  %60 = icmp ne i8 %59, 0
  %phitmp = zext i1 %60 to i8
  %61 = select i1 %58, i8 %phitmp, i8 1
  %62 = call fastcc zeroext i8 @safe_mod_func_uint8_t_u_u(i8 zeroext 42, i8 zeroext %61)
  store i32 1, i32* %0, align 4, !tbaa !6
  call void @llvm.lifetime.end.p0i8(i64 8, i8* nonnull %6) #5
  ret i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 4)
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i8* @func_24(i16 signext %0, i16 zeroext %1, i32 %2) unnamed_addr #0 {
  ret i8* @g_20
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
  %.02 = phi i32 [ 0, %1 ], [ %11, %8 ]
  %7 = icmp ult i32 %.02, 4
  br i1 %7, label %8, label %12

8:                                                ; preds = %6
  %9 = zext i32 %.02 to i64
  %10 = getelementptr inbounds [4 x i32], [4 x i32]* %2, i64 0, i64 %9
  store i32 -4, i32* %10, align 4, !tbaa !6
  %11 = add nuw nsw i32 %.02, 1
  br label %6

12:                                               ; preds = %22, %6
  %.1 = phi i32 [ %23, %22 ], [ 0, %6 ]
  %13 = icmp ult i32 %.1, 2
  br i1 %13, label %14, label %24

14:                                               ; preds = %20, %12
  %.01 = phi i32 [ %21, %20 ], [ 0, %12 ]
  %15 = icmp ult i32 %.01, 4
  br i1 %15, label %16, label %22

16:                                               ; preds = %18, %14
  %.0 = phi i32 [ %19, %18 ], [ 0, %14 ]
  %17 = icmp ult i32 %.0, 2
  br i1 %17, label %18, label %20

18:                                               ; preds = %16
  %19 = add nuw nsw i32 %.0, 1
  br label %16

20:                                               ; preds = %16
  %21 = add nuw nsw i32 %.01, 1
  br label %14

22:                                               ; preds = %14
  %23 = add nuw nsw i32 %.1, 1
  br label %12

24:                                               ; preds = %12
  %25 = zext i8 %0 to i64
  %26 = call fastcc i8* @func_39(i64 %25, i8** nonnull @g_44, i8* null)
  %27 = load i32, i32* @g_171, align 4, !tbaa !6
  %28 = sext i32 %27 to i64
  %29 = call fastcc i64 @safe_sub_func_int64_t_s_s(i64 1, i64 %28)
  %30 = trunc i64 %29 to i32
  %31 = getelementptr inbounds [4 x i32], [4 x i32]* %2, i64 0, i64 2
  %32 = load i32, i32* %31, align 8, !tbaa !6
  %33 = trunc i32 %32 to i16
  %34 = load i8, i8* %3, align 1, !tbaa !8
  %35 = call fastcc i32* @func_34(i32 %30, i8* null, i16 zeroext %33, i8 signext %34)
  store i32* %35, i32** @g_215, align 8, !tbaa !0
  store volatile i32* %35, i32** getelementptr inbounds ([7 x [2 x i32*]], [7 x [2 x i32*]]* @g_211, i64 0, i64 4, i64 1), align 8, !tbaa !0
  %36 = load i32, i32* %5, align 4, !tbaa !6
  store i32 %36, i32* %35, align 4, !tbaa !6
  br i1 icmp eq (i16* inttoptr (i64 trunc (i128 lshr (i128 bitcast (<2 x i64> <i64 ptrtoint (i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 7) to i64), i64 ptrtoint (i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 7) to i64)> to i128), i128 64) to i64) to i16*), i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 1)), label %37, label %52

37:                                               ; preds = %24
  %38 = load i16, i16* getelementptr inbounds ([8 x [7 x i16]], [8 x [7 x i16]]* @g_89, i64 0, i64 0, i64 0), align 16, !tbaa !9
  %39 = trunc i16 %38 to i8
  %40 = load i16, i16* @g_58, align 2, !tbaa !9
  %41 = trunc i16 %40 to i8
  %42 = load i8, i8* @g_111, align 1, !tbaa !8
  %43 = and i8 %42, %41
  store i8 %43, i8* @g_111, align 1, !tbaa !8
  %44 = call fastcc zeroext i8 @safe_add_func_uint8_t_u_u(i8 zeroext %39, i8 zeroext %43)
  %45 = zext i8 %44 to i16
  store i16 %45, i16* @g_58, align 2, !tbaa !9
  %46 = zext i8 %0 to i16
  %47 = call fastcc signext i16 @safe_mul_func_int16_t_s_s(i16 signext %45, i16 signext %46)
  %48 = call fastcc zeroext i16 @safe_mod_func_uint16_t_u_u(i16 zeroext %46, i16 zeroext 4)
  %49 = trunc i16 %48 to i8
  %50 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 1, i64 0, i64 0), align 4, !tbaa !6
  %51 = call fastcc signext i8 @safe_lshift_func_int8_t_s_u(i8 signext %49, i32 %50)
  br label %52

52:                                               ; preds = %37, %24
  %53 = phi i64 [ -7, %24 ], [ -8, %37 ]
  store i64 %53, i64* @g_11, align 8, !tbaa !4
  %54 = call fastcc i8* @func_39(i64 %53, i8** nonnull @g_44, i8* nonnull %3)
  %55 = call fastcc signext i8 @safe_rshift_func_int8_t_s_s(i8 signext 0, i32 1)
  %56 = load i32, i32* %5, align 4, !tbaa !6
  %57 = trunc i32 %56 to i8
  %58 = call fastcc signext i8 @safe_unary_minus_func_int8_t_s(i8 signext %57)
  %59 = sext i8 %58 to i32
  %60 = load volatile i32*, i32** @g_118, align 8, !tbaa !0
  store i32 %59, i32* %60, align 4, !tbaa !6
  call void @llvm.lifetime.end.p0i8(i64 1, i8* nonnull %3) #5
  call void @llvm.lifetime.end.p0i8(i64 16, i8* nonnull %4) #5
  ret i8* @g_20
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @safe_mod_func_int16_t_s_s(i16 signext %0, i16 signext %1) unnamed_addr #0 {
  %3 = icmp eq i16 %1, 0
  br i1 %3, label %7, label %4

4:                                                ; preds = %2
  %5 = icmp eq i16 %0, -32768
  %6 = icmp eq i16 %1, -1
  %or.cond = and i1 %5, %6
  br i1 %or.cond, label %7, label %9

7:                                                ; preds = %4, %2
  %8 = sext i16 %0 to i32
  br label %13

9:                                                ; preds = %4
  %10 = sext i16 %0 to i32
  %11 = sext i16 %1 to i32
  %12 = srem i32 %10, %11
  br label %13

13:                                               ; preds = %9, %7
  %14 = phi i32 [ %8, %7 ], [ %12, %9 ]
  %15 = trunc i32 %14 to i16
  ret i16 %15
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i8 @safe_lshift_func_uint8_t_u_s(i8 zeroext %0, i32 %1) unnamed_addr #0 {
  %3 = icmp slt i32 %1, 0
  %4 = icmp sgt i32 %1, 31
  %or.cond = or i1 %3, %4
  br i1 %or.cond, label %9, label %5

5:                                                ; preds = %2
  %6 = zext i8 %0 to i32
  %7 = lshr i32 255, %1
  %8 = icmp slt i32 %7, %6
  br i1 %8, label %9, label %11

9:                                                ; preds = %5, %2
  %10 = zext i8 %0 to i32
  br label %13

11:                                               ; preds = %5
  %12 = shl i32 %6, %1
  br label %13

13:                                               ; preds = %11, %9
  %14 = phi i32 [ %10, %9 ], [ %12, %11 ]
  %15 = trunc i32 %14 to i8
  ret i8 %15
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i16 @safe_rshift_func_int16_t_s_s(i16 signext %0, i32 %1) unnamed_addr #0 {
  %3 = sext i16 %0 to i32
  %4 = icmp slt i16 %0, 0
  %5 = icmp slt i32 %1, 0
  %or.cond = or i1 %4, %5
  %6 = icmp sgt i32 %1, 31
  %or.cond1 = or i1 %6, %or.cond
  %7 = ashr i32 %3, %1
  %8 = select i1 %or.cond1, i32 %3, i32 %7
  %9 = trunc i32 %8 to i16
  ret i16 %9
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i64 @safe_div_func_uint64_t_u_u(i64 %0, i64 %1) unnamed_addr #0 {
  %3 = icmp eq i64 %1, 0
  br i1 %3, label %6, label %4

4:                                                ; preds = %2
  %5 = udiv i64 %0, %1
  br label %6

6:                                                ; preds = %4, %2
  %7 = phi i64 [ %5, %4 ], [ %0, %2 ]
  ret i64 %7
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i16 @safe_add_func_uint16_t_u_u(i16 zeroext %0, i16 zeroext %1) unnamed_addr #0 {
  %3 = add i16 %1, %0
  ret i16 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i16 @safe_rshift_func_uint16_t_u_u(i16 zeroext %0, i32 %1) unnamed_addr #0 {
  %3 = icmp ugt i32 %1, 31
  %4 = zext i16 %0 to i32
  %5 = lshr i32 %4, %1
  %6 = select i1 %3, i32 %4, i32 %5
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
  %3 = icmp eq i8 %1, 0
  br i1 %3, label %7, label %4

4:                                                ; preds = %2
  %5 = icmp eq i8 %0, -128
  %6 = icmp eq i8 %1, -1
  %or.cond = and i1 %5, %6
  br i1 %or.cond, label %7, label %9

7:                                                ; preds = %4, %2
  %8 = sext i8 %0 to i32
  br label %13

9:                                                ; preds = %4
  %10 = sext i8 %0 to i32
  %11 = sext i8 %1 to i32
  %12 = sdiv i32 %10, %11
  br label %13

13:                                               ; preds = %9, %7
  %14 = phi i32 [ %8, %7 ], [ %12, %9 ]
  %15 = trunc i32 %14 to i8
  ret i8 %15
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i8* @func_39(i64 %0, i8** %1, i8* %2) unnamed_addr #0 {
  %.sroa.03 = alloca i8*
  br label %4

4:                                                ; preds = %6, %3
  %.0 = phi i32 [ 0, %3 ], [ %7, %6 ]
  %5 = icmp ult i32 %.0, 2
  br i1 %5, label %6, label %8

6:                                                ; preds = %4
  %7 = add nuw nsw i32 %.0, 1
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
  %36 = load i32, i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 7), align 4
  %37 = icmp ne i32 %36, 0
  %phitmp1 = zext i1 %37 to i64
  %38 = select i1 %35, i64 0, i64 %phitmp1
  %39 = call fastcc i64 @safe_mod_func_int64_t_s_s(i64 0, i64 %38)
  %40 = trunc i64 %39 to i32
  store i32 %40, i32* @g_172, align 4, !tbaa !6
  %41 = call fastcc i64 @safe_unary_minus_func_uint64_t_u(i64 1)
  store i32 %18, i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 7), align 4, !tbaa !6
  %.sroa.03.0.copyload = load volatile i8*, i8** getelementptr inbounds (%union.U0, %union.U0* @g_106, i64 0, i32 0), align 8, !tbaa.struct !11
  store volatile i8* %.sroa.03.0.copyload, i8** %.sroa.03, !tbaa.struct !11
  %.sroa.03.0..sroa.03.0. = load i8*, i8** %.sroa.03
  ret i8* %.sroa.03.0..sroa.03.0.
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc signext i8 @safe_lshift_func_int8_t_s_u(i8 signext %0, i32 %1) unnamed_addr #0 {
  %3 = sext i8 %0 to i32
  %4 = icmp slt i8 %0, 0
  %5 = icmp ugt i32 %1, 31
  %or.cond = or i1 %4, %5
  %6 = lshr i32 127, %1
  %7 = icmp slt i32 %6, %3
  %or.cond3 = or i1 %or.cond, %7
  %8 = shl i32 %3, %1
  %9 = select i1 %or.cond3, i32 %3, i32 %8
  %10 = trunc i32 %9 to i8
  ret i8 %10
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i64 @safe_sub_func_int64_t_s_s(i64 %0, i64 %1) unnamed_addr #0 {
  %3 = xor i64 %1, %0
  %4 = and i64 %3, -9223372036854775808
  %5 = xor i64 %4, %0
  %6 = sub nsw i64 %5, %1
  %7 = xor i64 %6, %1
  %8 = and i64 %7, %3
  %9 = icmp slt i64 %8, 0
  %10 = sub nsw i64 %0, %1
  %spec.select = select i1 %9, i64 %0, i64 %10
  ret i64 %spec.select
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i64 @safe_mod_func_int64_t_s_s(i64 %0, i64 %1) unnamed_addr #0 {
  %3 = icmp eq i64 %1, 0
  br i1 %3, label %9, label %4

4:                                                ; preds = %2
  %5 = icmp eq i64 %0, -9223372036854775808
  %6 = icmp eq i64 %1, -1
  %or.cond = and i1 %5, %6
  br i1 %or.cond, label %9, label %7

7:                                                ; preds = %4
  %8 = srem i64 %0, %1
  br label %9

9:                                                ; preds = %7, %4, %2
  %10 = phi i64 [ %8, %7 ], [ %0, %2 ], [ -9223372036854775808, %4 ]
  ret i64 %10
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i16 @safe_sub_func_uint16_t_u_u(i16 zeroext %0, i16 zeroext %1) unnamed_addr #0 {
  %3 = sub i16 %0, %1
  ret i16 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i16 @func_59(i16 zeroext %0, i64 %1, i8 zeroext %2, i8 zeroext %3, i8* %4) unnamed_addr #0 {
  %.sroa.0 = alloca [348 x i8], align 16
  %.sroa.4 = alloca [48 x i8], align 16
  %.sroa.0.0.sroa_idx8 = getelementptr inbounds [348 x i8], [348 x i8]* %.sroa.0, i64 0, i64 0
  call void @llvm.lifetime.start.p0i8(i64 348, i8* %.sroa.0.0.sroa_idx8)
  %.sroa.4.0.sroa_idx6 = getelementptr inbounds [48 x i8], [48 x i8]* %.sroa.4, i64 0, i64 0
  call void @llvm.lifetime.start.p0i8(i64 48, i8* %.sroa.4.0.sroa_idx6)
  %.sroa.0.0.sroa_idx1 = getelementptr inbounds [348 x i8], [348 x i8]* %.sroa.0, i64 0, i64 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %.sroa.0.0.sroa_idx1, i8* align 16 bitcast ([2 x [10 x [5 x i32]]]* @__const.func_59.l_169 to i8*), i64 348, i1 false)
  %.sroa.4.0.sroa_idx4 = getelementptr inbounds [48 x i8], [48 x i8]* %.sroa.4, i64 0, i64 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %.sroa.4.0.sroa_idx4, i8* align 16 bitcast (i32* getelementptr inbounds ([2 x [10 x [5 x i32]]], [2 x [10 x [5 x i32]]]* @__const.func_59.l_169, i64 0, i64 1, i64 7, i64 3) to i8*), i64 48, i1 false)
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
  %26 = or i32 %25, %11
  %27 = trunc i32 %26 to i16
  %28 = call fastcc zeroext i16 @safe_sub_func_uint16_t_u_u(i16 zeroext %10, i16 zeroext %27)
  %29 = zext i16 %28 to i32
  %30 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 0, i64 0, i64 1), align 4, !tbaa !6
  %31 = or i32 %30, %29
  %32 = and i32 %31, -909000219
  %33 = trunc i32 %32 to i8
  %34 = load i16, i16* getelementptr inbounds ([8 x [7 x i16]], [8 x [7 x i16]]* @g_89, i64 0, i64 6, i64 5), align 2, !tbaa !9
  %35 = zext i16 %34 to i32
  %36 = call fastcc signext i8 @safe_lshift_func_int8_t_s_u(i8 signext %33, i32 %35)
  %37 = sext i8 %36 to i32
  %38 = call fastcc signext i8 @safe_lshift_func_int8_t_s_u(i8 signext %8, i32 %37)
  %39 = load volatile i32*, i32** @g_118, align 8, !tbaa !0
  %40 = load i8, i8* @g_111, align 1, !tbaa !8
  %41 = zext i8 %40 to i32
  %42 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 1, i64 0, i64 1), align 4, !tbaa !6
  %43 = icmp sle i32 %42, %41
  %44 = zext i1 %43 to i8
  %45 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 0, i64 0, i64 1), align 4, !tbaa !6
  %46 = call fastcc zeroext i8 @safe_rshift_func_uint8_t_u_u(i8 zeroext %44, i32 %45)
  %47 = load i64, i64* @g_11, align 8, !tbaa !4
  %48 = trunc i64 %47 to i32
  %49 = call fastcc signext i16 @safe_rshift_func_int16_t_s_u(i16 signext %0, i32 %48)
  %50 = load i32, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 0, i64 0, i64 1), align 4, !tbaa !6
  %51 = icmp eq i32 %50, 1
  %52 = zext i1 %51 to i32
  %53 = load i32, i32* @g_142, align 4, !tbaa !6
  %54 = and i32 %52, %53
  store i32 %54, i32* @g_142, align 4, !tbaa !6
  %55 = load i16, i16* getelementptr inbounds ([8 x [7 x i16]], [8 x [7 x i16]]* @g_89, i64 0, i64 0, i64 3), align 2, !tbaa !9
  %.sroa.0.0.sroa_idx9 = getelementptr inbounds [348 x i8], [348 x i8]* %.sroa.0, i64 0, i64 0
  call void @llvm.lifetime.end.p0i8(i64 348, i8* %.sroa.0.0.sroa_idx9)
  %.sroa.4.0.sroa_idx7 = getelementptr inbounds [48 x i8], [48 x i8]* %.sroa.4, i64 0, i64 0
  call void @llvm.lifetime.end.p0i8(i64 48, i8* %.sroa.4.0.sroa_idx7)
  ret i16 %55
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc i8** @func_67(i16* %0, i16 signext %1, i8 zeroext %2, i8* %3, i32 %4) unnamed_addr #0 {
  %.sroa.0 = alloca [860 x i8], align 16
  %.sroa.4 = alloca [144 x i8], align 16
  %.sroa.0.0.sroa_idx9 = getelementptr inbounds [860 x i8], [860 x i8]* %.sroa.0, i64 0, i64 0
  call void @llvm.lifetime.start.p0i8(i64 860, i8* %.sroa.0.0.sroa_idx9)
  %.sroa.4.0.sroa_idx7 = getelementptr inbounds [144 x i8], [144 x i8]* %.sroa.4, i64 0, i64 0
  call void @llvm.lifetime.start.p0i8(i64 144, i8* %.sroa.4.0.sroa_idx7)
  %.sroa.0.0.sroa_idx2 = getelementptr inbounds [860 x i8], [860 x i8]* %.sroa.0, i64 0, i64 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %.sroa.0.0.sroa_idx2, i8* align 16 bitcast ([4 x [9 x [7 x i32]]]* @__const.func_67.l_117 to i8*), i64 860, i1 false)
  %.sroa.4.0.sroa_idx5 = getelementptr inbounds [144 x i8], [144 x i8]* %.sroa.4, i64 0, i64 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %.sroa.4.0.sroa_idx5, i8* align 16 bitcast (i32* getelementptr inbounds ([4 x [9 x [7 x i32]]], [4 x [9 x [7 x i32]]]* @__const.func_67.l_117, i64 0, i64 3, i64 3, i64 6) to i8*), i64 144, i1 false)
  br label %6

6:                                                ; preds = %8, %5
  %.0 = phi i32 [ 0, %5 ], [ %9, %8 ]
  %7 = icmp ult i32 %.0, 3
  br i1 %7, label %8, label %10

8:                                                ; preds = %6
  %9 = add nuw nsw i32 %.0, 1
  br label %6

10:                                               ; preds = %6
  store i32 -1835502843, i32* getelementptr inbounds ([2 x [1 x [7 x i32]]], [2 x [1 x [7 x i32]]]* @g_119, i64 0, i64 1, i64 0, i64 0), align 4, !tbaa !6
  %11 = load i16, i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 1), align 2, !tbaa !9
  %12 = add i16 %11, -1
  store i16 %12, i16* getelementptr inbounds ([8 x i16], [8 x i16]* @g_91, i64 0, i64 1), align 2, !tbaa !9
  %13 = icmp eq i16 %11, 0
  br i1 %13, label %20, label %14

14:                                               ; preds = %10
  store i64 1, i64* getelementptr inbounds ([4 x i64], [4 x i64]* @g_131, i64 0, i64 2), align 16, !tbaa !4
  %15 = load i32, i32* getelementptr inbounds ([9 x i32], [9 x i32]* @g_18, i64 0, i64 8), align 16, !tbaa !6
  %16 = trunc i32 %15 to i8
  store i8 %16, i8* @g_111, align 1, !tbaa !8
  %17 = call fastcc zeroext i8 @safe_rshift_func_uint8_t_u_u(i8 zeroext %16, i32 2)
  %18 = call fastcc signext i16 @safe_mod_func_int16_t_s_s(i16 signext 0, i16 signext -21917)
  %19 = call fastcc signext i8 @safe_mul_func_int8_t_s_s(i8 signext 114, i8 signext 0)
  br label %20

20:                                               ; preds = %14, %10
  %21 = call fastcc zeroext i16 @safe_sub_func_uint16_t_u_u(i16 zeroext 1, i16 zeroext 0)
  %.sroa.0.0.sroa_idx10 = getelementptr inbounds [860 x i8], [860 x i8]* %.sroa.0, i64 0, i64 0
  call void @llvm.lifetime.end.p0i8(i64 860, i8* %.sroa.0.0.sroa_idx10)
  %.sroa.4.0.sroa_idx8 = getelementptr inbounds [144 x i8], [144 x i8]* %.sroa.4, i64 0, i64 0
  call void @llvm.lifetime.end.p0i8(i64 144, i8* %.sroa.4.0.sroa_idx8)
  ret i8** null
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i8 @safe_sub_func_uint8_t_u_u(i8 zeroext %0, i8 zeroext %1) unnamed_addr #0 {
  %3 = sub i8 %0, %1
  ret i8 %3
}

; Function Attrs: minsize nounwind optsize uwtable
define internal fastcc zeroext i16 @safe_mod_func_uint16_t_u_u(i16 zeroext %0, i16 zeroext %1) unnamed_addr #0 {
  %3 = icmp eq i16 %1, 0
  br i1 %3, label %6, label %4

4:                                                ; preds = %2
  %5 = urem i16 %0, %1
  br label %6

6:                                                ; preds = %4, %2
  %.in = phi i16 [ %5, %4 ], [ %0, %2 ]
  ret i16 %.in
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
