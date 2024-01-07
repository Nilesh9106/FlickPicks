import { Button, Image } from "@nextui-org/react";
import { Link } from "react-router-dom";
import { AiFillHeart, AiOutlineHeart, AiOutlineLoading } from "react-icons/ai";
import { useState } from "react";
import { postCall } from "./api";

type Movie = {
    id: number,
    title: string,
    poster_path: string,
    release_date: string,
    genres: string,
    isFavorite: boolean
}

export default function MovieCard({ movie, onDelete }: { movie: Movie, onDelete?: () => void }) {
    const [isFav, setIsFav] = useState(movie.isFavorite);
    const [loading, setLoading] = useState(false);
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

                <Button
                    variant="shadow"
                    isIconOnly={true}
                    onClick={async (e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        if (loading) return;
                        setLoading(true);
                        if (isFav) {
                            const data = await postCall('movies/removeFromFav', { movie_id: movie.id });
                            if (data.status == "success") {
                                setIsFav(false);
                                if (onDelete) {
                                    onDelete();
                                }
                            }
                        } else {
                            const data = await postCall('movies/addToFav', { movie_id: movie.id });
                            if (data.status == "success") {
                                setIsFav(true);
                            }
                        }
                        setLoading(false);
                    }}
                    className="absolute top-3 right-3 z-50 p-1 bg-neutral-200 dark:bg-neutral-900 rounded-full transition-all duration-500"
                >
                    {loading ? <AiOutlineLoading className="animate-spin" /> : (isFav ? <AiFillHeart className="text-red-500 text-2xl" /> : <AiOutlineHeart className="text-2xl" />)}
                </Button>

            </div>
        </Link>
    );
}

