#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "./SDL_utils.h"

struct dbpendulum {
    float x1;
    float y1;

    float x2;
    float y2;

    float x3;
    float y3;

    float a1;
    float a2;

    float Va1;
    float Va2;

    float Aa1;
    float Aa2;

    float l;
    float m1;
    float m2;
};
typedef struct dbpendulum dbpendulum;

dbpendulum* dbpendulumCreate(float x1,
                             float y1,
                             float a1,
                             float a2,
                             float l,
                             float m1,
                             float m2);
void dbpendulumFree(dbpendulum* dbpd);
void stepDBPendulum(dbpendulum* dbpd, int upd);
void drawDBPendulum(SDL_Renderer* renderer, dbpendulum* dbpd, SDL_Color color);