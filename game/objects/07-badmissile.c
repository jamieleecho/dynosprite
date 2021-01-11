#ifdef __cplusplus
extern "C" {
#endif

#include "07-badmissile.h"
#include "03-badguy.h"
#include "04-ship.h"
#include "object_info.h"


static void checkHitShip(DynospriteCOB *cob);


static byte didInit = FALSE;
static DynospriteCOB *shipCob;


#ifdef __APPLE__
void BadmissileClassInit() {
    didInit = FALSE;
}
#endif


void BadmissileInit(DynospriteCOB *cob, DynospriteODT *odt, byte *initData) {
    if (!didInit) {
	didInit = TRUE;
    }
    DynospriteCOB *obj = DynospriteDirectPageGlobalsPtr->Obj_CurrentTablePtr;
    shipCob = findObjectByGroup(obj, SHIP_GROUP_IDX);
    BadMissileObjectState *statePtr = (BadMissileObjectState *)(cob->statePtr);
    statePtr->spriteIdx = 0;
}


byte BadmissileReactivate(DynospriteCOB *cob, DynospriteODT *odt) {
    //if (((ShipObjectState *)shipCob->statePtr)->counter != 0) {
    //    return 0;
    //}
    cob->globalY = 10;
    cob->active = OBJECT_ACTIVE;
    return 0;
}


byte BadmissileUpdate(DynospriteCOB *cob, DynospriteODT *odt) {
    if (cob->globalY > 180) {
        cob->globalY = 10;

        //if (((ShipObjectState *)shipCob->statePtr)->counter != 0) {
        //    cob->active = OBJECT_INACTIVE;
        //    return 0;
        //}
    } else {
        byte delta = ((DynospriteDirectPageGlobalsPtr->Obj_MotionFactor + 2)) << 1;
        cob->globalY += delta;
        checkHitShip(cob);
    }
    return 0;
}

static void checkHitShip(DynospriteCOB *cob) {
    if (!shipCob->active) {
        return;
    }
    
    int deltaX = shipCob->globalX - cob->globalX;
    int deltaY = shipCob->globalY - cob->globalY;
    int yy0 = deltaY - MISSILE_HEIGHT - SHIP_HALF_HEIGHT;
    int yy1 = deltaY + MISSILE_HEIGHT + SHIP_HALF_HEIGHT;
    byte didHit = FALSE;
    if ((yy0 <= 0) && (yy1 >= 0)) {
        int xx0 = deltaX - MISSILE_HALF_WIDTH - SHIP_THIN_HALF_WIDTH;
        int xx1 = deltaX + MISSILE_HALF_WIDTH + SHIP_THIN_HALF_WIDTH;
        if ((xx0 <= 0) && (xx1 >= 0)) {
            didHit = TRUE;
        }
    }
    
    int yy2 = deltaY - MISSILE_HEIGHT - SHIP_THICK_HALF_HEIGHT;
    if (!didHit && yy2 <= 0) {
        int xx2 = deltaX - MISSILE_HALF_WIDTH - SHIP_HALF_WIDTH;
        int xx3 = deltaX + MISSILE_HALF_WIDTH + SHIP_HALF_WIDTH;
        if ((xx2 <= 0) && (xx3 >= 0)) {
            didHit = TRUE;
        }
    }

    if (didHit) {
        ShipObjectState *statePtr = (ShipObjectState *)(shipCob->statePtr);
        if (statePtr->spriteIdx < SHIP_SPRITE_EXPLOSION_INDEX) {
            statePtr->spriteIdx = SHIP_SPRITE_EXPLOSION_INDEX;
            cob->globalX &= 0xfffe;
            //statePtr->counter = 128;
            //PlaySound(2);
        }
    }

    return;
}

RegisterObject(BadmissileClassInit, BadmissileInit, 0, BadmissileReactivate, BadmissileUpdate, sizeof(BadMissleObjectState));

#ifdef __cplusplus
}
#endif
