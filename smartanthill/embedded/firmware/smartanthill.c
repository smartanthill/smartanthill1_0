/**
 * Copyright (C) 2013-2014 Ivan Kravets <me@ikravets.com>
 * See LICENSE for details.
 */

#include "smartanthill.h"

void setup()
{
    UARTInit(9600);
}

void loop()
{
    routerLoop();

    if (routerHasInPacket())
        osm.makeTransition(osm.findStateByCDC(routerGetInPacket()->cdc));

    osm.updateState();
}
