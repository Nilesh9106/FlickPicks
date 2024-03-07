import React from 'react';
import { render } from '@testing-library/react';
import MovieSlider from '../src/components/MovieSlider';
import { describe, it } from 'vitest';

describe('MovieSlider', () => {
  const movies = [
    {
      id: 1,
      title: 'Test Movie 1',
      release_date: '2022-01-01',
      genres: 'Action',
      poster_path: 'test-poster1.jpg',
      isFavorite: false,
    },
    {
      id: 2,
      title: 'Test Movie 2',
      release_date: '2022-02-01',
      genres: 'Comedy',
      poster_path: 'test-poster2.jpg',
      isFavorite: true,
    },
  ];

  it('renders the movie slider correctly', () => {
    render(<MovieSlider movies={movies} />);
  });
});