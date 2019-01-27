//
//  DSLevel.m
//  Space Bandits
//
//  Created by Jamie Cho on 12/29/18.
//  Copyright © 2018 Jamie Cho. All rights reserved.
//

#import "DSLevel.h"

@implementation DSLevel

- (id)initWithInitLevel:(DSLevelInit)initLevel backgroundNewXY:(DSLevelBackgroundNewXY)backgroundNewXY {
    self = [super init];
    
    if (self) {
        _initLevel = initLevel;
        _backgroundNewXY = backgroundNewXY;
    }
    
    return self;
}

- (DSLevelInit)initLevel {
    return _initLevel;
}

- (DSLevelBackgroundNewXY)backgroundNewXY {
    return _backgroundNewXY;
}

@end