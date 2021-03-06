//
//  AppDelegate.h
//  dynosprite
//
//  Created by Jamie Cho on 12/29/18.
//  Copyright © 2018 Jamie Cho. All rights reserved.
//

#import <Cocoa/Cocoa.h>

#import "DSConfigFileParser.h"
#import "DSLevelFileParser.h"
#import "DSAssetLoader.h"
#import "DSSceneController.h"
#import "DSSoundManager.h"


@interface DSAppDelegate : NSObject <NSApplicationDelegate>

@property (nonatomic, nonnull) IBOutlet DSConfigFileParser *configFileParser;
@property (nonatomic, nonnull) IBOutlet DSAssetLoader *assetLoader;
@property (nonatomic, nonnull) IBOutlet DSSceneController *sceneController;
@property (nonatomic, nonnull) IBOutlet DSSoundManager *soundManager;

- (void)awakeFromNib;
- (BOOL)applicationShouldTerminateAfterLastWindowClosed:(NSApplication *_Null_unspecified)sender;

@end
