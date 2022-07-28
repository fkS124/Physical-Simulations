#include "../lib/dbpendulum.h"


dbpendulum* dbpendulumCreate(float x1, float y1, float a1, float a2, float l, float m1, float m2) {
    dbpendulum* dbpd = malloc(sizeof(*dbpd));

    dbpd->x1 = x1;
    dbpd->y1 = y1;

    dbpd->x2 = x1 + sin(a1) * l;
    dbpd->y2 = y1 + cos(a1) * l;

    dbpd->x3 = dbpd->x2 + sin(a2) * l;
    dbpd->y3 = dbpd->y2 + cos(a2) * l;

    dbpd->a1 = a1;
    dbpd->a2 = a2;

    dbpd->Va1 = 0.0f;
    dbpd->Va2 = 0.0f;

    dbpd->Aa1 = 0.0f;
    dbpd->Aa2 = 0.0f;

    dbpd->m1 = m1;
    dbpd->m2 = m2;
    dbpd->l = l;

    return dbpd;
}

void dbpendulumFree(dbpendulum* dbpd) {
    free(dbpd);
}


void stepDBPendulum(dbpendulum* dbpd, int upd) {
    if ( upd == -1 )
        return;

    // Get all the current state's values
    float g, l, num1, num2, num3, num4, den, a1, a2, m1, m2, Va1, Va2;
    g = 9.81f;
    a1 = dbpd->a1;
    a2 = dbpd->a2;
    Va1 = dbpd->Va1;
    Va2 = dbpd->Va2;
    m1 = dbpd->m1;
    m2 = dbpd->m2;
    l = dbpd->l;

    // Calculate the acceleration of the first angle
    num1 = -g * (2 * m1 + m2) * sin(a1);
    num2 = -m2 * g * sin(a1 - 2 * a2);
    num3 = -2 * sin(a1 - a2) * m2;
    num4 = pow(Va2, 2) * l + pow(Va1, 2) * l * cos(a1 - a2);
    den = l * (2 * m1 * m2 - m2 * cos(2 * a1 - 2 * a2)); 
    dbpd->Aa1 = (num1 + num2 + num3 * num4)/den;
    
    // Calculate the acceleration of the second angle
    num1 = 2 * sin(a1 - a2);
    num2 = pow(Va1, 2) * l * (m1 + m2);
    num3 = g * (m1 + m2) * cos(a1);
    num4 = pow(Va2, 2) * l * m2 * cos(a1 - a2);
    den = l * (2 * m1 * m2 - m2 * cos(2 * a1 - 2 * a2));
    dbpd->Aa2 = (num1 * (num2 + num3 + num4)) / den;

    // Apply Euler's method to find the solution and therefore 
    // move the double pendulum using an approximation of the exact
    // answer.
    dbpd->Va1 += dbpd->Aa1;
    dbpd->a1 += dbpd->Va1;

    dbpd->Va2 += dbpd->Aa2;
    dbpd->a2 += dbpd->Va2;

    // Then recalculate the positions of all the vertexes
    dbpd->x2 = dbpd->x1 + sin(dbpd->a1) * l;
    dbpd->y2 = dbpd->y1 + cos(dbpd->a1) * l;

    dbpd->x3 = dbpd->x2 + sin(dbpd->a2) * l;
    dbpd->y3 = dbpd->y2 + cos(dbpd->a2) * l;
}

void drawDBPendulum(SDL_Renderer* renderer, dbpendulum* dbpd, SDL_Color color) {
    drawLine( renderer, dbpd->x1, dbpd->y1, dbpd->x2, dbpd->y2, color );
    drawLine( renderer, dbpd->x2, dbpd->y2, dbpd->x3, dbpd->y3, color );
}