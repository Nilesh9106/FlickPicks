import { Image } from "@nextui-org/react";
import { Link } from "react-router-dom";


type Movie = {
    id: number,
    title: string,
    poster_path: string,
    release_date: string,
    genres: string,
}

export default function MovieCard({ movie }: { movie: Movie }) {
    return (
        <Link to={`/movie/${movie.id}`}>
            <div className="relative group h-full overflow-hidden rounded-lg mx-3 cursor-pointer">
                <Image
                    radius="md"
                    alt="Movie"
                    className="object-cover w-full pointer-events-none group-hover:scale-105 transition-all duration-500"
                    src={movie.poster_path}
                />
                <div className="absolute group-hover:bottom-0 -bottom-8 max-sm:-bottom-7 transition-all w-full  z-50 p-3 bg-neutral-200/20 dark:bg-neutral-900/20 backdrop-blur-md rounded-t-lg ">
                    <div className="text-lg max-sm:text-sm font-bold line-clamp-1">{movie.title}</div>
                    <div className="text-sm max-sm:text-xs">{movie.release_date}</div>
                    <div className="text-sm line-clamp-1 max-sm:text-xs">{movie.genres}</div>
                </div>
            </div>
        </Link>
    );
}

