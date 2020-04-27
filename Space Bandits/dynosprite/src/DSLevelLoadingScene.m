//
//  DSLevelLoadingScene.m
//  Space Bandits
//
//  Created by Jamie Cho on 4/26/20.
//  Copyright © 2020 Jamie Cho. All rights reserved.
//

#import "DSLevelLoadingScene.h"

@implementation DSLevelLoadingScene

- (id)init {
    if (self = [super init]) {
        self.bundle = NSBundle.mainBundle;
    }
    return self;
}

- (void)didMoveToView:(SKView *)view {
    [super didMoveToView:view];
    self.isDone = NO;
    if (self.labels.count == 0) {
        NSImage *backgroundImage = [[NSImage alloc] initWithContentsOfFile:[self.bundle pathForResource:@"images/01-level1" ofType:@"png"]];
        
        const float y0 = ((((200 - 64) - backgroundImage.size.height) / 3) / 2);
        const float y1 = y0 + backgroundImage.size.height;
        const float y2 = y1 + 16;
        const float y3 = y2 + 18;
        const float y4 = y3 + 14;
        
        self.backgroundImage.size = backgroundImage.size;
        self.backgroundImage.position = CGPointMake(159 - backgroundImage.size.width / 2.0f, -y0);
        
        SKLabelNode *levelNameLabel = [self addLabelWithText:self.levelName atPosition:CGPointMake(0, y1)];
        levelNameLabel.parent.position = CGPointMake(159 - (levelNameLabel.parent.frame.size.width / 2.0f), levelNameLabel.parent.frame.origin.y);

        SKLabelNode *levelDescriptionLabel = [self addLabelWithText:self.levelDescription atPosition:CGPointMake(0, y2)];
        levelDescriptionLabel.parent.position = CGPointMake(159 - (levelDescriptionLabel.parent.frame.size.width / 2.0f), levelDescriptionLabel.parent.frame.origin.y);

        SKLabelNode *levelLoadingLabel = [self addLabelWithText:@"Loading..." atPosition:CGPointMake(0, y4)];
        levelLoadingLabel.parent.position = CGPointMake(159 - (levelLoadingLabel.parent.frame.size.width / 2.0f), levelLoadingLabel.parent.frame.origin.y);
    }
}

@end
