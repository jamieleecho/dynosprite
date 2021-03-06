//
//  DSTileMapMaker.h
//  Space Bandits
//
//  Created by Jamie Cho on 5/2/20.
//  Copyright © 2020 Jamie Cho. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import <SpriteKit/SpriteKit.h>

#import "DSCons.h"

NS_ASSUME_NONNULL_BEGIN

@interface DSTileMapMaker : NSObject

- (NSImage *)subImage:(NSImage *)image withRect:(NSRect)rect;
- (NSImage *)subImageForMap:(NSImage *)image withRect:(NSRect)rect;
- (NSImage *)tileForImage:(NSImage *)image atPoint:(NSPoint)p0;
- (NSString *)hashForImage:(NSImage *)image;
- (BOOL)image:(NSImage *)image1 isEqualTo:(NSImage *)image2;
- (NSDictionary<NSString *, DSCons<NSImage *, NSNumber *> *> *)imageTileDictionaryFromImage:(NSImage *)image;
- (SKTextureAtlas *)atlasFromTileDictionary:(NSDictionary<NSString *, DSCons<NSImage *, NSNumber *> *> *)tileDictionary;
- (NSDictionary<NSNumber *, NSString *> *)tileIndexToTileHashFromTileDictionary:(NSDictionary<NSString *, DSCons<NSImage *, NSNumber *> *> *)tileDictionary;
- (SKTileSet *)tileSetFromTextureAtlas:(SKTextureAtlas *)textureAtlas;
- (SKTileMapNode *)nodeFromImage:(NSImage *)image withRect:(NSRect)rect usingTileImage:(NSImage *)tileImage withTileRect:(NSRect)tileRect;

@end

NS_ASSUME_NONNULL_END
