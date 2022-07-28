#include "../lib/SDL_utils.h"


void drawLine(SDL_Renderer* renderer, int x1, int y1, int x2, int y2, SDL_Color color) {
	if ( SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a) != 0 )
		SDL_ExitWithError( "Couldn't set the renderer's color" );
	if ( SDL_RenderDrawLine(renderer, x1, y1, x2, y2) != 0 )
		SDL_ExitWithError( "Couldn't draw the line." );
}


void SDL_ExitWithError(const char * message)
{
    printf("Error : %s > %s \n", message, SDL_GetError());
    SDL_Quit();
    exit(EXIT_FAILURE);
}

