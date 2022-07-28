#include "./lib/dbpendulum.h"

#define WIDTH 500
#define HEIGHT 500
#define PI 3.1415


int main( int argc, char* argv[] )  {
	int running, lastUpdated, dep_mass1, end_mass1, dep_mass2, end_mass2, l, np;
	float angle1, angle2;
	SDL_Color dep_color, end_color;

	if ( SDL_Init( SDL_INIT_EVERYTHING ) != 0 ) {
		SDL_ExitWithError( "Couldn't init SDL2" );
	}

	SDL_Window* window = NULL;
	SDL_Renderer* renderer = NULL;

	window = SDL_CreateWindow( "Double Pendulum Simulation",
								SDL_WINDOWPOS_UNDEFINED,
								SDL_WINDOWPOS_UNDEFINED,
								WIDTH, HEIGHT, SDL_WINDOW_ALLOW_HIGHDPI );

	if ( window == NULL )
		SDL_ExitWithError( "Couldn't initialize SDL window" );

	renderer = SDL_CreateRenderer( window, -1, SDL_RENDERER_PRESENTVSYNC | SDL_RENDERER_SOFTWARE );

	if ( renderer == NULL )
		SDL_ExitWithError( "Couldn't initialize SDL renderer" );

	running = 1;
	lastUpdated = 0;
	SDL_Color pdColorTest = {255, 255, 255};

	np = 10000;
	float k = sqrt(np / 1000);
	dep_mass1 = 240;
	dep_mass2 = 200;
	end_mass1 = dep_mass1+80*k;
	end_mass2 = dep_mass2+80*k;
	l = 100;
	angle1 = PI/2;
	angle2 = PI/2;
	dep_color.r = 255;
	dep_color.g = 0;
	dep_color.b = 0;
	end_color.r = 0;
	end_color.g = 255;
	end_color.b = 0;

	dbpendulum **allPendulums = calloc(np, sizeof(dbpendulum));
	SDL_Color *allColors = calloc(np, sizeof(SDL_Color));
	float counter = -1.0f;

	for (int i = 0; i < np; i++) {
		counter++;
		float ratio = counter / np;
		float m1 = dep_mass1 + (end_mass1 - dep_mass1) * ratio;
		float m2 = dep_mass2 + (end_mass2 - dep_mass2) * ratio;

		allPendulums[i] = dbpendulumCreate( WIDTH/2, HEIGHT/2, angle1, angle2, l, m1, m2);
		allColors[i].r = dep_color.r + (end_color.r - dep_color.r) * i / np;
		allColors[i].g = dep_color.g + (end_color.g - dep_color.g) * i / np;
		allColors[i].b = dep_color.b + (end_color.b - dep_color.b) * i / np;
	}
	printf("Succesfully initialized %d double pendulums.", np);

	int typeRun = -1;

	while ( running ) {
		SDL_Event event;

		while ( SDL_PollEvent( &event ) ) {
			switch( event.type ) {
				case SDL_QUIT:
					running = 0;
					break;

				case SDL_KEYDOWN:
					switch ( event.key.keysym.sym ) {
						case SDLK_SPACE:
							typeRun = typeRun == -1 ? 1 : -1;
							break;
						default:
							break;
					}
					break;

				default:
					break;
			}
		}
		// Fills the renderer
		SDL_SetRenderDrawColor( renderer, 0, 0, 0, 255 );
		// Clears the renderer
		SDL_RenderClear( renderer );

		// draws the pendulum
		for ( int i = 0; i < np; i++ ) drawDBPendulum( renderer, allPendulums[i], allColors[i] );

		if ( SDL_GetTicks() - lastUpdated > 1/30 ) {
			lastUpdated = SDL_GetTicks();
			for ( int i = 0; i < np; i++ ) stepDBPendulum( allPendulums[i], typeRun );
		}

		// updates the screen
		SDL_RenderPresent( renderer );
	}


	for ( int i = 0; i < np; i++ ) dbpendulumFree( allPendulums[i] );
	free( allColors );
	free( allPendulums );
	SDL_DestroyRenderer( renderer );
	SDL_DestroyWindow( window );
	SDL_Quit( );

	return 0;
}


