//
//  InitScene.h
//  dynosprite
//
//  Created by Jamie Cho on 1/6/19.
//  Copyright © 2019 Jamie Cho. All rights reserved.
//

#import "DSTransitionScene.h"
#import "DSTransitionSceneControllerProtocol.h"

NS_ASSUME_NONNULL_BEGIN

typedef enum DSInitSceneDisplay {
    DSInitSceneDisplayLow,
    DSInitSceneDisplayHigh
} DSInitSceneDisplay;

typedef enum DSInitSceneControl {
    DSInitSceneControlKeyboard,
DSInitSceneControlJoystick
} DSInitSceneControl;

typedef enum DSInitSceneSound {
    DSInitSceneSoundLow,
    DSInitSceneSoundHigh
} DSInitSceneSound;

@interface DSInitScene : DSTransitionScene {
    SKLabelNode *_resolutionLabelNode;
    SKLabelNode *_controlLabelNode;
    SKLabelNode *_soundLabelNode;
    
    DSInitSceneDisplay _resolution;
    DSInitSceneControl _control;
    DSInitSceneSound _sound;
}
+ (NSString *)textFromResolution:(DSInitSceneDisplay)resolution;
+ (NSString *)textFromControl:(DSInitSceneControl)control;
+ (NSString *)textFromSound:(DSInitSceneSound)sound;

@property (nonatomic) id<DSTransitionSceneControllerProtocol> transitionSceneController;

- (void)didMoveToView:(SKView *)view;
- (void)willMoveFromView:(SKView *)view;

- (void)mouseUp:(NSEvent *)theEvent;
- (void)keyUp:(NSEvent *)theEvent;

- (void)transitionToNextScreen;

- (void)toggleDisplay;
- (DSInitSceneDisplay)display;

- (void)toggleControl;
- (DSInitSceneControl)control;

- (void)toggleSound;
- (DSInitSceneSound)sound;

- (void)poll;

@end

NS_ASSUME_NONNULL_END
