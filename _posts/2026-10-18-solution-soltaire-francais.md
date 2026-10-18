---
layout: post
title:  "Solution solitaire Français"
date:   2026-10-18 17:00:00 +0200
categories: stuff
---

# Solitaire français (37 billes)

Solution en **35 coups** : départ en retirant **C1**, arrivée avec une seule bille en **E4**.

**Légende :** `●` bille · `○` trou vide · colonnes A→G (gauche→droite), lignes 1→7 (haut→bas).

Notation `e1-c1` : la bille en E1 saute par-dessus D1, atterrit en C1, et D1 est retirée.

## Plateau de départ

Plateau plein (37 billes) :

```
    A B C D E F G
1       ● ● ●
2     ● ● ● ● ●
3   ● ● ● ● ● ● ●
4   ● ● ● ● ● ● ●
5   ● ● ● ● ● ● ●
6     ● ● ● ● ●
7       ● ● ●
```

## Étape 0 — retirer C1

```
    A B C D E F G
1       ○ ● ●
2     ● ● ● ● ●
3   ● ● ● ● ● ● ●
4   ● ● ● ● ● ● ●
5   ● ● ● ● ● ● ●
6     ● ● ● ● ●
7       ● ● ●
```

## Coup 1 — `e1-c1`

Saute E1 → C1, retire D1. Billes restantes : 35.

```
    A B C D E F G
1       ● ○ ○
2     ● ● ● ● ●
3   ● ● ● ● ● ● ●
4   ● ● ● ● ● ● ●
5   ● ● ● ● ● ● ●
6     ● ● ● ● ●
7       ● ● ●
```

## Coup 2 — `d3-d1`

Saute D3 → D1, retire D2. Billes restantes : 34.

```
    A B C D E F G
1       ● ● ○
2     ● ● ○ ● ●
3   ● ● ● ○ ● ● ●
4   ● ● ● ● ● ● ●
5   ● ● ● ● ● ● ●
6     ● ● ● ● ●
7       ● ● ●
```

## Coup 3 — `d5-d3`

Saute D5 → D3, retire D4. Billes restantes : 33.

```
    A B C D E F G
1       ● ● ○
2     ● ● ○ ● ●
3   ● ● ● ● ● ● ●
4   ● ● ● ○ ● ● ●
5   ● ● ● ○ ● ● ●
6     ● ● ● ● ●
7       ● ● ●
```

## Coup 4 — `f2-d2`

Saute F2 → D2, retire E2. Billes restantes : 32.

```
    A B C D E F G
1       ● ● ○
2     ● ● ● ○ ○
3   ● ● ● ● ● ● ●
4   ● ● ● ○ ● ● ●
5   ● ● ● ○ ● ● ●
6     ● ● ● ● ●
7       ● ● ●
```

## Coup 5 — `b4-d4`

Saute B4 → D4, retire C4. Billes restantes : 31.

```
    A B C D E F G
1       ● ● ○
2     ● ● ● ○ ○
3   ● ● ● ● ● ● ●
4   ● ○ ○ ● ● ● ●
5   ● ● ● ○ ● ● ●
6     ● ● ● ● ●
7       ● ● ●
```

## Coup 6 — `b2-b4`

Saute B2 → B4, retire B3. Billes restantes : 30.

```
    A B C D E F G
1       ● ● ○
2     ○ ● ● ○ ○
3   ● ○ ● ● ● ● ●
4   ● ● ○ ● ● ● ●
5   ● ● ● ○ ● ● ●
6     ● ● ● ● ●
7       ● ● ●
```

## Coup 7 — `f5-d5`

Saute F5 → D5, retire E5. Billes restantes : 29.

```
    A B C D E F G
1       ● ● ○
2     ○ ● ● ○ ○
3   ● ○ ● ● ● ● ●
4   ● ● ○ ● ● ● ●
5   ● ● ● ● ○ ○ ●
6     ● ● ● ● ●
7       ● ● ●
```

## Coup 8 — `f3-f5`

Saute F3 → F5, retire F4. Billes restantes : 28.

```
    A B C D E F G
1       ● ● ○
2     ○ ● ● ○ ○
3   ● ○ ● ● ● ○ ●
4   ● ● ○ ● ● ○ ●
5   ● ● ● ● ○ ● ●
6     ● ● ● ● ●
7       ● ● ●
```

## Coup 9 — `c2-e2`

Saute C2 → E2, retire D2. Billes restantes : 27.

```
    A B C D E F G
1       ● ● ○
2     ○ ○ ○ ● ○
3   ● ○ ● ● ● ○ ●
4   ● ● ○ ● ● ○ ●
5   ● ● ● ● ○ ● ●
6     ● ● ● ● ●
7       ● ● ●
```

## Coup 10 — `c6-c4`

Saute C6 → C4, retire C5. Billes restantes : 26.

```
    A B C D E F G
1       ● ● ○
2     ○ ○ ○ ● ○
3   ● ○ ● ● ● ○ ●
4   ● ● ● ● ● ○ ●
5   ● ● ○ ● ○ ● ●
6     ● ○ ● ● ●
7       ● ● ●
```

## Coup 11 — `c1-e1`

Saute C1 → E1, retire D1. Billes restantes : 25.

```
    A B C D E F G
1       ○ ○ ●
2     ○ ○ ○ ● ○
3   ● ○ ● ● ● ○ ●
4   ● ● ● ● ● ○ ●
5   ● ● ○ ● ○ ● ●
6     ● ○ ● ● ●
7       ● ● ●
```

## Coup 12 — `b5-b3`

Saute B5 → B3, retire B4. Billes restantes : 24.

```
    A B C D E F G
1       ○ ○ ●
2     ○ ○ ○ ● ○
3   ● ● ● ● ● ○ ●
4   ● ○ ● ● ● ○ ●
5   ● ○ ○ ● ○ ● ●
6     ● ○ ● ● ●
7       ● ● ●
```

## Coup 13 — `d4-b4`

Saute D4 → B4, retire C4. Billes restantes : 23.

```
    A B C D E F G
1       ○ ○ ●
2     ○ ○ ○ ● ○
3   ● ● ● ● ● ○ ●
4   ● ● ○ ○ ● ○ ●
5   ● ○ ○ ● ○ ● ●
6     ● ○ ● ● ●
7       ● ● ●
```

## Coup 14 — `d3-f3`

Saute D3 → F3, retire E3. Billes restantes : 22.

```
    A B C D E F G
1       ○ ○ ●
2     ○ ○ ○ ● ○
3   ● ● ● ○ ○ ● ●
4   ● ● ○ ○ ● ○ ●
5   ● ○ ○ ● ○ ● ●
6     ● ○ ● ● ●
7       ● ● ●
```

## Coup 15 — `e6-c6`

Saute E6 → C6, retire D6. Billes restantes : 21.

```
    A B C D E F G
1       ○ ○ ●
2     ○ ○ ○ ● ○
3   ● ● ● ○ ○ ● ●
4   ● ● ○ ○ ● ○ ●
5   ● ○ ○ ● ○ ● ●
6     ● ● ○ ○ ●
7       ● ● ●
```

## Coup 16 — `g5-e5`

Saute G5 → E5, retire F5. Billes restantes : 20.

```
    A B C D E F G
1       ○ ○ ●
2     ○ ○ ○ ● ○
3   ● ● ● ○ ○ ● ●
4   ● ● ○ ○ ● ○ ●
5   ● ○ ○ ● ● ○ ○
6     ● ● ○ ○ ●
7       ● ● ●
```

## Coup 17 — `e4-e6`

Saute E4 → E6, retire E5. Billes restantes : 19.

```
    A B C D E F G
1       ○ ○ ●
2     ○ ○ ○ ● ○
3   ● ● ● ○ ○ ● ●
4   ● ● ○ ○ ○ ○ ●
5   ● ○ ○ ● ○ ○ ○
6     ● ● ○ ● ●
7       ● ● ●
```

## Coup 18 — `e7-e5`

Saute E7 → E5, retire E6. Billes restantes : 18.

```
    A B C D E F G
1       ○ ○ ●
2     ○ ○ ○ ● ○
3   ● ● ● ○ ○ ● ●
4   ● ● ○ ○ ○ ○ ●
5   ● ○ ○ ● ● ○ ○
6     ● ● ○ ○ ●
7       ● ● ○
```

## Coup 19 — `c7-c5`

Saute C7 → C5, retire C6. Billes restantes : 17.

```
    A B C D E F G
1       ○ ○ ●
2     ○ ○ ○ ● ○
3   ● ● ● ○ ○ ● ●
4   ● ● ○ ○ ○ ○ ●
5   ● ○ ● ● ● ○ ○
6     ● ○ ○ ○ ●
7       ○ ● ○
```

## Coup 20 — `d5-b5`

Saute D5 → B5, retire C5. Billes restantes : 16.

```
    A B C D E F G
1       ○ ○ ●
2     ○ ○ ○ ● ○
3   ● ● ● ○ ○ ● ●
4   ● ● ○ ○ ○ ○ ●
5   ● ● ○ ○ ● ○ ○
6     ● ○ ○ ○ ●
7       ○ ● ○
```

## Coup 21 — `a5-c5`

Saute A5 → C5, retire B5. Billes restantes : 15.

```
    A B C D E F G
1       ○ ○ ●
2     ○ ○ ○ ● ○
3   ● ● ● ○ ○ ● ●
4   ● ● ○ ○ ○ ○ ●
5   ○ ○ ● ○ ● ○ ○
6     ● ○ ○ ○ ●
7       ○ ● ○
```

## Coup 22 — `e1-e3`

Saute E1 → E3, retire E2. Billes restantes : 14.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ○ ○ ○ ○
3   ● ● ● ○ ● ● ●
4   ● ● ○ ○ ○ ○ ●
5   ○ ○ ● ○ ● ○ ○
6     ● ○ ○ ○ ●
7       ○ ● ○
```

## Coup 23 — `a4-c4`

Saute A4 → C4, retire B4. Billes restantes : 13.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ○ ○ ○ ○
3   ● ● ● ○ ● ● ●
4   ○ ○ ● ○ ○ ○ ●
5   ○ ○ ● ○ ● ○ ○
6     ● ○ ○ ○ ●
7       ○ ● ○
```

## Coup 24 — `c4-c2`

Saute C4 → C2, retire C3. Billes restantes : 12.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ● ○ ○ ○
3   ● ● ○ ○ ● ● ●
4   ○ ○ ○ ○ ○ ○ ●
5   ○ ○ ● ○ ● ○ ○
6     ● ○ ○ ○ ●
7       ○ ● ○
```

## Coup 25 — `a3-c3`

Saute A3 → C3, retire B3. Billes restantes : 11.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ● ○ ○ ○
3   ○ ○ ● ○ ● ● ●
4   ○ ○ ○ ○ ○ ○ ●
5   ○ ○ ● ○ ● ○ ○
6     ● ○ ○ ○ ●
7       ○ ● ○
```

## Coup 26 — `c2-c4`

Saute C2 → C4, retire C3. Billes restantes : 10.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ○ ○ ○ ○
3   ○ ○ ○ ○ ● ● ●
4   ○ ○ ● ○ ○ ○ ●
5   ○ ○ ● ○ ● ○ ○
6     ● ○ ○ ○ ●
7       ○ ● ○
```

## Coup 27 — `c4-c6`

Saute C4 → C6, retire C5. Billes restantes : 9.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ○ ○ ○ ○
3   ○ ○ ○ ○ ● ● ●
4   ○ ○ ○ ○ ○ ○ ●
5   ○ ○ ○ ○ ● ○ ○
6     ● ● ○ ○ ●
7       ○ ● ○
```

## Coup 28 — `b6-d6`

Saute B6 → D6, retire C6. Billes restantes : 8.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ○ ○ ○ ○
3   ○ ○ ○ ○ ● ● ●
4   ○ ○ ○ ○ ○ ○ ●
5   ○ ○ ○ ○ ● ○ ○
6     ○ ○ ● ○ ●
7       ○ ● ○
```

## Coup 29 — `d7-d5`

Saute D7 → D5, retire D6. Billes restantes : 7.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ○ ○ ○ ○
3   ○ ○ ○ ○ ● ● ●
4   ○ ○ ○ ○ ○ ○ ●
5   ○ ○ ○ ● ● ○ ○
6     ○ ○ ○ ○ ●
7       ○ ○ ○
```

## Coup 30 — `d5-f5`

Saute D5 → F5, retire E5. Billes restantes : 6.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ○ ○ ○ ○
3   ○ ○ ○ ○ ● ● ●
4   ○ ○ ○ ○ ○ ○ ●
5   ○ ○ ○ ○ ○ ● ○
6     ○ ○ ○ ○ ●
7       ○ ○ ○
```

## Coup 31 — `f6-f4`

Saute F6 → F4, retire F5. Billes restantes : 5.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ○ ○ ○ ○
3   ○ ○ ○ ○ ● ● ●
4   ○ ○ ○ ○ ○ ● ●
5   ○ ○ ○ ○ ○ ○ ○
6     ○ ○ ○ ○ ○
7       ○ ○ ○
```

## Coup 32 — `g4-e4`

Saute G4 → E4, retire F4. Billes restantes : 4.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ○ ○ ○ ○
3   ○ ○ ○ ○ ● ● ●
4   ○ ○ ○ ○ ● ○ ○
5   ○ ○ ○ ○ ○ ○ ○
6     ○ ○ ○ ○ ○
7       ○ ○ ○
```

## Coup 33 — `e4-e2`

Saute E4 → E2, retire E3. Billes restantes : 3.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ○ ○ ● ○
3   ○ ○ ○ ○ ○ ● ●
4   ○ ○ ○ ○ ○ ○ ○
5   ○ ○ ○ ○ ○ ○ ○
6     ○ ○ ○ ○ ○
7       ○ ○ ○
```

## Coup 34 — `g3-e3`

Saute G3 → E3, retire F3. Billes restantes : 2.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ○ ○ ● ○
3   ○ ○ ○ ○ ● ○ ○
4   ○ ○ ○ ○ ○ ○ ○
5   ○ ○ ○ ○ ○ ○ ○
6     ○ ○ ○ ○ ○
7       ○ ○ ○
```

## Coup 35 — `e2-e4`

Saute E2 → E4, retire E3. Billes restantes : 1.

```
    A B C D E F G
1       ○ ○ ○
2     ○ ○ ○ ○ ○
3   ○ ○ ○ ○ ○ ○ ○
4   ○ ○ ○ ○ ● ○ ○
5   ○ ○ ○ ○ ○ ○ ○
6     ○ ○ ○ ○ ○
7       ○ ○ ○
```

## Résultat

Une seule bille reste, en **E4**.
