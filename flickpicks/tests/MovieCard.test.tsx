import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import MovieCard from '../src/components/MovieCard';
import { describe, expect, it } from 'vitest';
import * as matchers from '@testing-library/jest-dom/matchers';
expect.extend(matchers);

describe('MovieCard', () => {
  const movie = {
    id: 1,
    title: 'Test Movie',
    release_date: '2022-01-01',
    genres: 'Action',
    poster_path: 'test-poster.jpg',
    isFavorite: false,
  };

  it('renders the movie card correctly', () => {

    render(
        <MemoryRouter>
            <MovieCard movie={movie} />
        </MemoryRouter>
    );

    // Assert that the movie title is rendered
    expect(screen.getByText('Test Movie')).toBeInTheDocument();

    // Assert that the movie release date is rendered
    expect(screen.getByText('2022-01-01')).toBeInTheDocument();

    // Assert that the movie genres are rendered
    expect(screen.getByText('Action')).toBeInTheDocument();

    // Assert that the movie poster is rendered
    expect(screen.getByAltText('Movie')).toHaveAttribute('src', 'test-poster.jpg');
  });
});