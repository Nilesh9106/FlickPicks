import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { getCall, tmdbGetCall } from "../../components/api";
import { AiFillStar } from "react-icons/ai";
import { Image } from "@nextui-org/react";
import MovieSlider from "../../components/MovieSlider";
import Loading from "../../components/Loading";

type Movie = {
    id: number,
    title: string,
    poster_path: string,
    release_date: string,
    genres: string,
    isFavorite: boolean
}
type MovieDetails = {
    id: number,
    title: string,
    poster_path: string,
    release_date: string,
    genres: string,
    isFavorite: boolean,
    overview: string,
    runtime: number,
    tagline: string,
    budget: number,
    revenue: number,
    keywords: string,
    production_companies: string,
    status: string,
    vote_average: number,
}

type Video = {
    key: string,
    name: string,
    site: string,
    size: number,
    type: string,
    official: boolean,
    published_at: string,
}

export default function Movie() {
    const [loading, setLoading] = useState(false)
    const [movie, setMovie] = useState<MovieDetails>()
    const [recommendations, setRecommendations] = useState([] as Movie[])
    const [videos, setVideos] = useState([] as Video[])
    const { id } = useParams()
    useEffect(() => {
        fetchMovie();
        console.info("Movie fetching...");
    }, [id])

    const fetchMovie = async () => {
        setLoading(true);
        const data = await getCall(`movies/${id}`);
        if (data.status == "success") {
            setMovie(data.movie);
            setRecommendations(data.recommendations);
            const videos = await tmdbGetCall(`movie/${id}/videos`);
            setVideos(videos.results);
        }
        console.info("Movie fetched");
        setLoading(false);
    }
    return (
        loading ? <Loading /> : (
            <div className="container lg:px-40 md:px-32 sm:px-10 px-3 w-full flex flex-col justify-center gap-2 py-4 ">
                <div className="flex justify-between my-2">
                    <div>
                        <h2 className="sm:text-4xl text-xl">{movie?.title}</h2>
                        <p className="text-medium max-sm:text-sm ">{movie?.release_date}</p>
                    </div>
                    <div className="flex gap-1 flex-col">
                        <p>RATING</p>
                        <div className="flex gap-1 items-center max-sm:text-sm">
                            <AiFillStar className="text-3xl text-yellow-500" /> <span className="text-nowrap max-sm:text-xs">{movie?.vote_average}/10</span>
                        </div>
                    </div>
                </div>
                <div className="flex flex-wrap gap-4">
                    <Image
                        radius="md"
                        alt="Movie"
                        isBlurred
                        className="object-cover sm:h-[25rem] max-sm:w-full pointer-events-none transition-all duration-500"
                        src={movie?.poster_path}
                    />
                    {
                        videos.length > 0 && <div className="">
                            <h2 className="md:hidden text-xl my-2">Video</h2>
                            <iframe src={`https://www.youtube.com/embed/${videos[0]?.key}`} className="rounded-md sm:h-[25rem] max-sm:w-full aspect-video" ></iframe>
                        </div>
                    }
                </div>

                <div className="flex flex-col gap-2">
                    <h2 className="text-xl my-2">Overview</h2>
                    <p className="text-medium max-sm:text-sm ">{movie?.overview}</p>

                    <hr className="my-1" />
                    <h2 className="text-xl my-2">Genres</h2>
                    <p className="text-medium max-sm:text-sm ">{movie?.genres}</p>

                    {
                        movie?.keywords && movie?.keywords != "0" && <>
                            <hr className="my-1" />
                            <h2 className="text-xl my-2">Keywords</h2>
                            <p className="text-medium max-sm:text-sm ">{movie?.keywords}</p>
                        </>
                    }

                    <hr className="my-1" />
                    <h2 className="text-xl my-2">Production Companies</h2>
                    <p className="text-medium max-sm:text-sm ">{movie?.production_companies}</p>

                    <hr className="my-1" />
                    <h2 className="text-xl my-2">Status</h2>
                    <p className="text-medium max-sm:text-sm ">{movie?.status}</p>

                    <hr className="my-1" />
                    <h2 className="text-xl my-2">Runtime</h2>
                    <p className="text-medium max-sm:text-sm ">{movie?.runtime} minutes</p>

                    <hr className="my-1" />
                    <h2 className="text-xl my-2">Budget</h2>
                    <p className="text-medium max-sm:text-sm ">${movie?.budget}</p>

                    <hr className="my-1" />
                    <h2 className="text-xl my-2">Revenue</h2>
                    <p className="text-medium max-sm:text-sm ">${movie?.revenue}</p>
                </div>

                <div>
                    <h3 className="text-2xl px-3 py-6 font-bold line-clamp-1">Movies Like {movie?.title}</h3>
                    <MovieSlider movies={recommendations} />
                </div>
            </div>
        )

    )

}
