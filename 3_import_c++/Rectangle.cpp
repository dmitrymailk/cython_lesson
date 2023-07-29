#include <iostream>
#include "Rectangle.h"

namespace shapes
{

	// Default constructor
	Rectangle::Rectangle() {}

	// Overloaded constructor
	Rectangle::Rectangle(int x0, int y0, int x1, int y1)
	{
		this->x0 = x0;
		this->y0 = y0;
		this->x1 = x1;
		this->y1 = y1;
	}

	// Destructor
	Rectangle::~Rectangle()
	{
		printf("Object deconstruction....\n");
	}

	// Move the rectangle by dx dy
	void Rectangle::move(int dx, int dy)
	{
		printf("Moving...\n");
		this->x0 += dx;
		this->y0 += dy;
		this->x1 += dx;
		this->y1 += dy;
	}

	void Rectangle::print()
	{
		printf("x0=%d y0=%d x1=%d y1=%d\n", this->x0, this->y0, this->x1, this->y1);
	}
}