//
//  08-shipcounter.c
//  Space Bandits
//
//  Created by Jamie Cho on 2/18/21.
//  Copyright © 2021 Jamie Cho. All rights reserved.
//

#include "dynosprite.h"
#include "object_info.h"
#include "08-shipcounter.h"


GameGlobals *globals;


#ifdef __APPLE__
void ShipcounterClassInit() {
}
#endif


void ShipcounterInit(DynospriteCOB *cob, DynospriteODT *odt, byte *initData) {
    globals = (GameGlobals *)&DynospriteGlobalsPtr->UserGlobals_Init;
    ShipCounterObjectState *state = (ShipCounterObjectState *)cob->statePtr;
    state->spriteIdx = 0;
    state->numShips = initData[0];
}


byte ShipcounterReactivate(DynospriteCOB *cob, DynospriteODT *odt) {
    cob->active = (((ShipCounterObjectState *)cob->statePtr)->numShips <= globals->numShips) ? OBJECT_ACTIVE : OBJECT_INACTIVE;
    return 0;
}


byte ShipcounterUpdate(DynospriteCOB *cob, DynospriteODT *odt) {
    cob->active = (((ShipCounterObjectState *)cob->statePtr)->numShips <= globals->numShips) ? OBJECT_ACTIVE : OBJECT_INACTIVE;
    return 0;
}


RegisterObject(ShipcounterClassInit, ShipcounterInit, 0, ShipcounterReactivate, ShipcounterUpdate, NULL, sizeof(ShipCounterObjectState));
