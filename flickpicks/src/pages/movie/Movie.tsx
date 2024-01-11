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


type Video = {
    key: string,
    name: string,
    site: string,
    size: number,
    type: string,
    official: boolean,
    published_at: string,
}
type MovieDetails = {
    id: number,
    title: string,
    poster_path: string,
    release_date: string,
    genres: [{ name: string }],
    isFavorite: boolean,
    overview: string,
    runtime: number,
    tagline: string,
    budget: number,
    revenue: number,
    keywords: [{ name: string }],
    production_companies: [{ name: string }],
    status: string,
    vote_average: number,
    videos: { results: [Video] }
}

export default function Movie() {
    const [loading, setLoading] = useState(false)
    const [movie, setMovie] = useState<MovieDetails>()
    const [recommendations, setRecommendations] = useState([] as Movie[])
    const { id } = useParams()
    useEffect(() => {
        fetchMovie();
        console.info("Movie fetching...");
    }, [id])

    const fetchMovie = async () => {
        setLoading(true);
        const data = await getCall(`movies/${id}`);
        if (data.status == "success") {
            setRecommendations(data.recommendations);
            const movies = await tmdbGetCall(`movie/${id}`, "append_to_response=videos");
            console.log(movies);
            setMovie(movies);
        }
        console.info("Movie fetched");
        setLoading(false);
    }
    return (
        loading ? <Loading /> : (
            <div className="xl:px-32 md:px-20  sm:px-10 px-3 w-full flex flex-col justify-center gap-2 py-4 ">
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
                <div className="flex max-lg:flex-wrap gap-4">
                    <Image
                        radius="md"
                        alt="Movie"
                        isBlurred
                        className="object-cover sm:h-[25rem] max-sm:w-full pointer-events-none transition-all duration-500"
                        src={"https://image.tmdb.org/t/p/original" + movie?.poster_path}
                    />
                    {
                        movie && movie.videos.results.length > 0 && <div className="">
                            <h2 className="md:hidden text-xl my-2">Video</h2>
                            <iframe src={`https://www.youtube.com/embed/${movie.videos.results[0]?.key}`} className="rounded-md sm:h-[20rem] xl:h-[25rem] max-sm:w-full aspect-video" ></iframe>
                        </div>
                    }
                </div>

                <div className="flex flex-col gap-2">
                    <h2 className="text-xl my-2">Overview</h2>
                    <p className="text-medium max-sm:text-sm ">{movie?.overview}</p>

                    <hr className="my-1" />
                    <h2 className="text-xl my-2">Genres</h2>
                    <p className="text-medium max-sm:text-sm ">{movie?.genres.map((genre) => `${genre.name}, `)}</p>

                    {
                        movie?.keywords && <>
                            <hr className="my-1" />
                            <h2 className="text-xl my-2">Keywords</h2>
                            <p className="text-medium max-sm:text-sm ">{movie?.keywords.map((keyword) => `${keyword.name}, `)}</p>
                        </>
                    }

                    <hr className="my-1" />
                    <h2 className="text-xl my-2">Production Companies</h2>
                    <p className="text-medium max-sm:text-sm ">{movie?.production_companies.map((company) => `${company.name}, `)}</p>

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
