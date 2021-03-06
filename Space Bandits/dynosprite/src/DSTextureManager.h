//
//  DSTextureManager.h
//  Space Bandits
//
//  Created by Jamie Cho on 12/31/20.
//  Copyright © 2020 Jamie Cho. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <SpriteKit/SpriteKit.h>
#import "dynosprite.h"
#import "DSTexture.h"
#import "DSSpriteObjectClass.h"
#import "DSResourceController.h"


NS_ASSUME_NONNULL_BEGIN

@interface DSTextureManager : NSObject {
    NSMutableDictionary<NSNumber *, NSArray<DSTexture *> *> *_groupIdToTextures;
}

@property (nonatomic) NSBundle *bundle;
@property (nonatomic) IBOutlet DSResourceController *resourceController;

- (id)init;
- (void)addSpriteObjectClass:(DSSpriteObjectClass *)spriteObjectClass;
- (void)configureSprite:(SKSpriteNode *)node forCob:(DynospriteCOB *)cob andScene:(SKScene *)scene andCamera:(SKCameraNode *)camera;

@end

NS_ASSUME_NONNULL_END
