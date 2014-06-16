/**
 * Copyright (C) Ivan Kravets <me@ikravets.com>
 * See LICENSE for details.
 */

#include "main.h"

/* int freeRam () {*/
/*   extern int __heap_start, *__brkval;*/
/*   int v;*/
/*   return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);*/
/* }*/


void setup()
{
    routerInit();
    /* Serial.println(freeRam());*/
}

void loop()
{
    routerLoop();

    if (routerHasInPacket())
        osm.makeTransition(osm.findStateByCDC(routerGetInPacket()->cdc));

    osm.updateState();
}
