#include <stdio.h>

#include "h-define.h"
#include "h-type.h"
#include "defines.h"
#include "externs.h"


#include "wadstructs.h"

int cave_sector_map[DUNGEON_HGT][DUNGEON_WID];

int sector_counter=-1; /* preallocated */
int vertex_counter=0; /* postallocated */
int linedef_counter=-1; /* preallocated */
int sidedef_counter=-1; /* preallocated */
int thing_counter=0; /* postallocated */
int tag_counter=0; /* postallocated */
int max_linedefs=0;
Thing *things=NULL;
Vertex *vertexes=NULL;
Linedef *linedefs=NULL;
Sidedef *sidedefs=NULL;
Sector *sectors=NULL;
int vertex_idx[DUNGEON_HGT][DUNGEON_WID];

void visualize() 
{
	int x, y;
	

	// ROCK1 for walls
	// RROCK13 for floor/ceiling
	// 1 tile = 64 units square
	// tunnel hight should be 64 units
	// light level 64 is nice and dark...

	for(y=0; y < DUNGEON_HGT - 1 ; y++) {
		for(x=0; x < DUNGEON_WID - 1; x++) {
			if(cave_sector_map[y][x] != cave_sector_map[y][x+1]) {
			    printf("v:%d:%d\n",x*3+3, y*3);
			}
			if(cave_sector_map[y][x] != cave_sector_map[y+1][x]) {
				printf("h:%d:%d\n",x*3, y*3+3);
			}			
		}
	}

}

void add_thing(Thing* t) 
{
	things=(Thing*)realloc(things, ++thing_counter * sizeof(Thing));
	memcpy(&things[thing_counter-1], t, sizeof(Thing));
}

int is_floor(int feat)
{
	return (feat == FEAT_FLOOR 
			|| feat == FEAT_LESS
			|| feat == FEAT_MORE
			|| feat == FEAT_TRAP_HEAD);
}

int is_floor_ish(int feat)
{
	return (feat == FEAT_FLOOR 
			|| feat == FEAT_DOOR_HEAD
			|| feat == FEAT_SECRET
			|| feat == FEAT_LESS
			|| feat == FEAT_MORE
			|| feat == FEAT_TRAP_HEAD);
}

int is_door(int feat) 
{
	return (feat == FEAT_DOOR_HEAD
			|| feat == FEAT_SECRET);
}

/* direction should be 0 for horizontal walls and 1 for vertical walls */
void do_linedef(int y, int x, int ye, int xe, int direction) 
{
	/* walls */
	if((cave_feat[y][x] >= FEAT_MAGMA && is_floor_ish(cave_feat[ye][xe]))
	   || (is_floor_ish(cave_feat[y][x]) && cave_feat[ye][xe] >= FEAT_MAGMA)) {

		linedefs[++linedef_counter].flags=0;
		linedefs[linedef_counter].type=0;
		linedefs[linedef_counter].tag=0;
		linedefs[linedef_counter].right_sidedef_idx=++sidedef_counter;
		linedefs[linedef_counter].left_sidedef_idx=-1;

		sidedefs[sidedef_counter].x_texture_off=0;
		sidedefs[sidedef_counter].y_texture_off=0;
		memset(sidedefs[sidedef_counter].upper_texture, 0, 8);
		memset(sidedefs[sidedef_counter].lower_texture, 0, 8);
		memset(sidedefs[sidedef_counter].normal_texture, 0, 8);
		memcpy(sidedefs[sidedef_counter].upper_texture, "ROCK1", 5);
		memcpy(sidedefs[sidedef_counter].lower_texture, "ROCK1", 5);
		memcpy(sidedefs[sidedef_counter].normal_texture, "ROCK1", 5);

		if(vertex_idx[ye][xe]==-1) vertex_idx[ye][xe]=vertex_counter++;
		if(vertex_idx[y+1][x+1]==-1) vertex_idx[y+1][x+1]=vertex_counter++;
		
		/* wall left/top, floor right/bottom */
		if(cave_feat[y][x] >= FEAT_MAGMA && is_floor_ish(cave_feat[ye][xe])) {
			if(direction) {	
				linedefs[linedef_counter].from_vertex=vertex_idx[y+1][x+1];
				linedefs[linedef_counter].to_vertex=vertex_idx[ye][xe];
			} else {
				linedefs[linedef_counter].from_vertex=vertex_idx[ye][xe];
				linedefs[linedef_counter].to_vertex=vertex_idx[y+1][x+1];
			}
			sidedefs[sidedef_counter].sector=cave_sector_map[ye][xe];
		}

		/* floor left/top, wall right/bottom */
		if(is_floor_ish(cave_feat[y][x]) && cave_feat[ye][xe] >= FEAT_MAGMA) {
			if(direction) {	
				linedefs[linedef_counter].to_vertex=vertex_idx[y+1][x+1];
				linedefs[linedef_counter].from_vertex=vertex_idx[ye][xe];
			} else {
				linedefs[linedef_counter].to_vertex=vertex_idx[ye][xe];
				linedefs[linedef_counter].from_vertex=vertex_idx[y+1][x+1];
			}
			sidedefs[sidedef_counter].sector=cave_sector_map[y][x];
		}

		return;
	}

	/* doors */
	if((is_floor(cave_feat[y][x]) && is_door(cave_feat[ye][xe]))
	   || (is_door(cave_feat[y][x]) && is_floor(cave_feat[ye][xe])))
	{
		linedef_counter++;
		
		if(vertex_idx[ye][xe]==-1) vertex_idx[ye][xe]=vertex_counter++;
		if(vertex_idx[y+1][x+1]==-1) vertex_idx[y+1][x+1]=vertex_counter++;

		linedefs[linedef_counter].flags=0x4;
		linedefs[linedef_counter].type=1;
		linedefs[linedef_counter].right_sidedef_idx=++sidedef_counter;
		
		/* door left/top, floor right/bottom */
		if(is_door(cave_feat[y][x]) && is_floor(cave_feat[ye][xe])) {
			if(direction) {	
				linedefs[linedef_counter].from_vertex=vertex_idx[y+1][x+1];
				linedefs[linedef_counter].to_vertex=vertex_idx[ye][xe];
			} else {
				linedefs[linedef_counter].from_vertex=vertex_idx[ye][xe];
				linedefs[linedef_counter].to_vertex=vertex_idx[y+1][x+1];
			}
			sidedefs[sidedef_counter].sector=cave_sector_map[ye][xe];
			sidedefs[sidedef_counter+1].sector=cave_sector_map[y][x];
		}

		/* floor left/top, door right/bottom */
		if(is_floor(cave_feat[y][x]) && is_door(cave_feat[ye][xe])) {
			if(direction) {	
				linedefs[linedef_counter].to_vertex=vertex_idx[y+1][x+1];
				linedefs[linedef_counter].from_vertex=vertex_idx[ye][xe];
			} else {
				linedefs[linedef_counter].to_vertex=vertex_idx[ye][xe];
				linedefs[linedef_counter].from_vertex=vertex_idx[y+1][x+1];
			}
			sidedefs[sidedef_counter].sector=cave_sector_map[y][x];
			sidedefs[sidedef_counter+1].sector=cave_sector_map[ye][xe];
		}		
					
		sidedefs[sidedef_counter].x_texture_off=0;
		sidedefs[sidedef_counter].y_texture_off=0;
		memset(sidedefs[sidedef_counter].upper_texture, 0, 8);
		memset(sidedefs[sidedef_counter].lower_texture, 0, 8);
		memset(sidedefs[sidedef_counter].normal_texture, 0, 8);
		memcpy(sidedefs[sidedef_counter].lower_texture, "-", 1);
		memcpy(sidedefs[sidedef_counter].normal_texture, "-", 1);

		linedefs[linedef_counter].left_sidedef_idx=++sidedef_counter;

		sidedefs[sidedef_counter].x_texture_off=0;
		sidedefs[sidedef_counter].y_texture_off=0;
		memset(sidedefs[sidedef_counter].upper_texture, 0, 8);
		memset(sidedefs[sidedef_counter].lower_texture, 0, 8);
		memset(sidedefs[sidedef_counter].normal_texture, 0, 8);
		memcpy(sidedefs[sidedef_counter].upper_texture, "-", 1);
		memcpy(sidedefs[sidedef_counter].lower_texture, "-", 1);
		memcpy(sidedefs[sidedef_counter].normal_texture, "-", 1);

		if(cave_feat[y][x] == FEAT_SECRET
		   || cave_feat[ye][xe] == FEAT_SECRET) {
			memcpy(sidedefs[sidedef_counter-1].upper_texture, "ROCK1", 5);
			linedefs[linedef_counter].flags |= 0x20;
		} else {
			memcpy(sidedefs[sidedef_counter-1].upper_texture, "WOODMET1", 8);
		}

		if(is_door(cave_feat[ye][xe]))
		{
			if(sectors[cave_sector_map[ye][xe]].tag == -1) sectors[cave_sector_map[ye][xe]].tag=tag_counter++;
			linedefs[linedef_counter].tag = sectors[cave_sector_map[ye][xe]].tag;
			sectors[cave_sector_map[ye][xe]].ceiling_height=0;
		} 
		if(is_door(cave_feat[y][x]))
		{
			if(sectors[cave_sector_map[y][x]].tag == -1) sectors[cave_sector_map[y][x]].tag=tag_counter++;
			linedefs[linedef_counter].tag = sectors[cave_sector_map[y][x]].tag;
			sectors[cave_sector_map[y][x]].ceiling_height=0;
		}

		return;
	}

	/* floor left/top, floor right/top */
	if(is_floor_ish(cave_feat[y][x])
	   && is_floor_ish(cave_feat[ye][xe])) {

		if(vertex_idx[ye][xe]==-1) vertex_idx[ye][xe]=vertex_counter++;
		if(vertex_idx[y+1][x+1]==-1) vertex_idx[y+1][x+1]=vertex_counter++;

		linedefs[++linedef_counter].from_vertex=vertex_idx[ye][xe];
		linedefs[linedef_counter].to_vertex=vertex_idx[y+1][x+1];

		linedefs[linedef_counter].flags=0x4;
		linedefs[linedef_counter].type=0;
		linedefs[linedef_counter].tag=0;
		linedefs[linedef_counter].right_sidedef_idx=++sidedef_counter;
					
		sidedefs[sidedef_counter].x_texture_off=0;
		sidedefs[sidedef_counter].y_texture_off=0;
		memset(sidedefs[sidedef_counter].upper_texture, 0, 8);
		memset(sidedefs[sidedef_counter].lower_texture, 0, 8);
		memset(sidedefs[sidedef_counter].normal_texture, 0, 8);
		memcpy(sidedefs[sidedef_counter].upper_texture, "-", 1);
		memcpy(sidedefs[sidedef_counter].lower_texture, "-", 1);
		memcpy(sidedefs[sidedef_counter].normal_texture, "-", 1);
		sidedefs[sidedef_counter].sector=cave_sector_map[ye][xe];

		linedefs[linedef_counter].left_sidedef_idx=++sidedef_counter;

		sidedefs[sidedef_counter].x_texture_off=0;
		sidedefs[sidedef_counter].y_texture_off=0;
		memset(sidedefs[sidedef_counter].upper_texture, 0, 8);
		memset(sidedefs[sidedef_counter].lower_texture, 0, 8);
		memset(sidedefs[sidedef_counter].normal_texture, 0, 8);
		memcpy(sidedefs[sidedef_counter].upper_texture, "-", 1);
		memcpy(sidedefs[sidedef_counter].lower_texture, "-", 1);
		memcpy(sidedefs[sidedef_counter].normal_texture, "-", 1);
		sidedefs[sidedef_counter].sector=cave_sector_map[y][x];

		return;
	}

}

void optimize_linedefs() 
{
	int i, n, dxi, dyi, dxn, dyn;

	for(i=0; i < linedef_counter; i++) {
		for(n=0; n < linedef_counter; n++) {
			if(linedefs[i].to_vertex == linedefs[n].from_vertex) {
				dxi=vertexes[linedefs[i].to_vertex].x - vertexes[linedefs[i].from_vertex].x;
				dyi=vertexes[linedefs[i].to_vertex].y - vertexes[linedefs[i].from_vertex].y;
				dxn=vertexes[linedefs[n].to_vertex].x - vertexes[linedefs[n].from_vertex].x;
				dyn=vertexes[linedefs[n].to_vertex].y - vertexes[linedefs[n].from_vertex].y;
				if((dxi * dyn) == (dyi * dxn)) {
					if((dxi * dyn) != 0
					   || (dxi == 0 && dxn == 0)
					   || (dyi == 0 && dyn == 0)) {
						if(linedefs[i].flags == linedefs[n].flags
						   && linedefs[i].type == linedefs[n].type
						   && linedefs[i].tag == linedefs[n].tag
						   && memcmp(&sidedefs[linedefs[i].right_sidedef_idx],
									 &sidedefs[linedefs[n].right_sidedef_idx],
									 sizeof(Sidedef))==0) {
							linedefs[i].to_vertex=linedefs[n].to_vertex;
							memcpy(&linedefs[n], &linedefs[linedef_counter--], sizeof(Linedef));
							i--;
							break;
						}
					}
				}
			}
		}
	}
}


void write_lump_entry(FILE* file, int start, int size, char* name) 
{
	Lump_Entry l;

	l.lump_start=start;
	l.lump_size=size;
	memset(l.lump_name, 0, 8);
	memcpy(l.lump_name, name, strlen(name));

	fwrite(&l, sizeof(Lump_Entry), 1, file);
}


void vectorize() 
{
	int x, y, i, start_ld_counter, old_ld_counter;

	for(y=0; y < DUNGEON_HGT; y++) {
		for(x=0; x < DUNGEON_WID; x++) {
			vertex_idx[y][x]=-1;
		}
	}

	for(y=0; y < DUNGEON_HGT - 1 ; y++) {
		for(x=0; x < DUNGEON_WID - 1; x++) {
			if(cave_sector_map[y][x] != cave_sector_map[y][x+1]) {
				max_linedefs++;
			}
			if(cave_sector_map[y][x] != cave_sector_map[y+1][x]) {
				max_linedefs++;
			}
		}
	}

	linedefs=(Linedef*)malloc((max_linedefs) * sizeof(Linedef));
	sidedefs=(Sidedef*)malloc((max_linedefs) * 2 * sizeof(Sidedef));

	sectors=(Sector*)malloc((sector_counter+1) * sizeof(Sector));

	for(i=0; i <= sector_counter; i++) {
		sectors[i].floor_height=0;
		sectors[i].ceiling_height=72;
		memset(sectors[i].floor_texture, 0, 8);
		memset(sectors[i].ceiling_texture, 0, 8);
		memcpy(sectors[i].floor_texture, "RROCK13", 7);
		memcpy(sectors[i].ceiling_texture, "RROCK13", 7);
		sectors[i].brightness=96;
		sectors[i].special=0;
		sectors[i].tag=-1;
	}

	for(y=0; y < DUNGEON_HGT - 1 ; y++) {
		for(x=0; x < DUNGEON_WID - 1; x++) {

			if(cave_sector_map[y][x] != cave_sector_map[y][x+1]) {
				do_linedef(y, x, y, x+1, 0);
			}

			if(cave_sector_map[y][x] != cave_sector_map[y+1][x]) {
				do_linedef(y, x, y+1, x, 1);
			}

			if(cave_feat[y][x]==FEAT_TRAP_HEAD) {
				sectors[cave_sector_map[y][x]].special += 0x10;
			}
		}		
	}

	vertexes=(Vertex*)malloc(vertex_counter * sizeof(Vertex));

	for(y=0; y < DUNGEON_HGT; y++) {
		for(x=0; x < DUNGEON_WID; x++) {
			if(vertex_idx[y][x] > -1) {
				vertexes[vertex_idx[y][x]].x = x * 64;
				vertexes[vertex_idx[y][x]].y = y * 64;
			}
		}
	}

	fflush(stdout);

	start_ld_counter=linedef_counter;
	do {
		old_ld_counter=linedef_counter;
		optimize_linedefs();
		fflush(stdout);
	} while(old_ld_counter != linedef_counter);


	visualize();
}
