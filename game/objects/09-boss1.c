//
//  09-boss1.c
//  Space Bandits
//
//  Created by Jamie Cho on 3/14/21.
//  Copyright © 2021 Jamie Cho. All rights reserved.
//

#include "dynosprite.h"
#include "object_info.h"
#include "09-boss1.h"


typedef enum Boss1MoveMode {
    Boss1MoveModeRight = 0,
    Boss1MoveModeLeft = 1
} Boss1MoveMode;


static GameGlobals *globals;
static byte frameCounter = 0;
const static byte phases[] = {
    0x0, 0x1, 0x2, 0x2, 0x1, 0x0
};
static byte /* Boss1MoveMode */ moveMode;


#ifdef __APPLE__
void Boss1ClassInit() {
    globals = NULL;
}
#endif


void Boss1Init(DynospriteCOB *cob, DynospriteODT *odt, byte *initData) {
    if (!globals) {
        globals = (GameGlobals *)DynospriteGlobalsPtr;
        Boss1ObjectState *state = (Boss1ObjectState *)cob->statePtr;
        state->spriteIdx = 0;
        state->currentPhase = 0;
        state->resetPhase = 0xff;
        moveMode = Boss1MoveModeRight;
    }
}


byte Boss1Reactivate(DynospriteCOB *cob, DynospriteODT *odt) {
    if (globals->gameWave == GameWavePerseiBoss) {
        cob->active = OBJECT_ACTIVE;
    }
    return 0;
}


byte Boss1Update(DynospriteCOB *cob, DynospriteODT *odt) {
    byte timeDelta = ((DynospriteDirectPageGlobalsPtr->Obj_MotionFactor + 2));
    byte delta = timeDelta * 3;
    if (delta > 12) {
        delta = 12;
    }

    frameCounter += timeDelta;
    if (frameCounter >= BOSS1_SPRITE_EXPLOSTION_INDEX) {
        frameCounter = 0x0;
    }
    Boss1ObjectState *state = (Boss1ObjectState *)cob->statePtr;
    if (frameCounter == 0) {
        if (++state->currentPhase >= sizeof(phases)/sizeof(phases[0])) {
            state->currentPhase = 0;
        }
        if (state->currentPhase == state->resetPhase) {
            state->resetPhase = 0xff;
        }
        
        (((Boss1ObjectState *)(cob->statePtr))->spriteIdx) = (state->resetPhase == 0xff ? 0 : BOSS1_SPRITE_EXPLOSTION_INDEX) + phases[state->currentPhase];
    }
    
    if (globals->gameState) {
        return 0;
    }
    
    if (moveMode == Boss1MoveModeRight) {
        cob->globalX += delta;
        if (cob->globalX > 320) {
            moveMode = Boss1MoveModeLeft;
            ++cob->globalY;
        }
    } else {
        cob->globalX -= delta;
        if (cob->globalX < 34) {
            moveMode = Boss1MoveModeRight;
            ++cob->globalY;
        }
    }

    return 0;
}


RegisterObject(Boss1ClassInit, Boss1Init, 0, Boss1Reactivate, Boss1Update, NULL, sizeof(Boss1ObjectState));
