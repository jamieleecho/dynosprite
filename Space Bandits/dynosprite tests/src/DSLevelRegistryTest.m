//
//  DSLevelRegistryTest.m
//  DynospriteCoreTests
//
//  Created by Jamie Cho on 12/29/18.
//  Copyright © 2018 Jamie Cho. All rights reserved.
//

#import <XCTest/XCTest.h>
#import "DSLevelRegistry.h"

@interface DSLevelRegistryTest : XCTestCase {
    DSLevelRegistry *_target;
    DSLevel *_level1;
    DSLevel *_level2;
}

@end


static void myLevel1Init(void) { }
static byte myLevel1BackgroundNewXY(void) { return 0; }
static void myLevel2Init(void) { }
static byte myLevel2BackgroundNewXY(void) { return 0; }


@implementation DSLevelRegistryTest

- (void)setUp {
    _target = [[DSLevelRegistry alloc] init];
    _level1 = [[DSLevel alloc] initWithInitLevel:myLevel1Init backgroundNewXY:myLevel1BackgroundNewXY];
    _level2 = [[DSLevel alloc] initWithInitLevel:myLevel2Init backgroundNewXY:myLevel2BackgroundNewXY];
}

- (void)tearDown {
    [DSLevelRegistry.sharedInstance clear];
}

- (void)testIndexFromFilename {
    XCTAssertEqual([DSLevelRegistry indexFromFilename:@"/foo01/bar/baz/07-thing-05.json"], 7);
    XCTAssertEqual([DSLevelRegistry indexFromFilename:@"/foo01/bar/baz/thing-05.json"], 0);
}

- (void)testSharedInstance {
    XCTAssertNotEqual(_target, DSLevelRegistry.sharedInstance);
    [DSLevelRegistry.sharedInstance addLevel:_level1 fromFile:@"01-foo.c"];
    XCTAssertEqual([DSLevelRegistry.sharedInstance levelForIndex:1], _level1);
}

- (void)testAddingAndRetrieving {
    XCTAssertNil([_target levelForIndex:5]);
    [_target addLevel:_level2 fromFile:@"/bar/23/baz/volumes /05-foo.c"];
    XCTAssertEqual([_target levelForIndex:5], _level2);
}

- (void)testClearing {
    [_target addLevel:_level2 fromFile:@"05-foo.c"];
    [_target clear];
    XCTAssertNil([_target levelForIndex:5]);
    XCTAssertEqual(_target.count, 0);
}

- (void)testCount {
    XCTAssertEqual(_target.count, 0);
    [_target addLevel:_level2 fromFile:@"02-foo.c"];
    XCTAssertEqual(_target.count, 1);
    [_target addLevel:_level1 fromFile:@"01-foo.c"];
    XCTAssertEqual(_target.count, 2);
}

@end
