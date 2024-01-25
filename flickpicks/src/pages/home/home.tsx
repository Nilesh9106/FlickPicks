import { useEffect, useState } from "react";
import { getCall } from "../../components/api"
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

export default function Home() {
    const [movies, setMovies] = useState({
        latest: [] as Movie[],
        action: [] as Movie[],
        bio: [] as Movie[],
    })
    const [recommendation, setRecommendation] = useState([] as Movie[])
    const [loading, setLoading] = useState(false)
    const getMovies = async () => {
        // fetch movies from api
        setLoading(true)
        const data = await getCall('movies');
        setRecommendation(data.recommendation ? data.recommendation : undefined)
        setMovies(
            {
                latest: data.latest,
                action: data.action,
                bio: data.bio
            }
        )
        setLoading(false)
    }

    useEffect(() => {
        getMovies()
    }, [])

    return (
        <>

            {loading && <Loading />}
            {!loading && (
                <div className="sm:px-8 px-4">
                    {
                        localStorage.getItem("token") && recommendation && recommendation.length > 0 && <div>
                            <h3 className="text-2xl px-3 py-6 font-bold">Movies for you</h3>
                            <MovieSlider movies={recommendation} />
                        </div>
                    }
                    <div>
                        <h3 className="text-2xl px-3 py-6 font-bold">Latest Movies</h3>
                        <MovieSlider movies={movies.latest} />
                    </div>
                    <div>
                        <h3 className="text-2xl px-3 py-6 font-bold">Action Movies</h3>
                        <MovieSlider movies={movies.action} />
                    </div>
                    <div>
                        <h3 className="text-2xl px-3 py-6 font-bold">Biography Movies</h3>
                        <MovieSlider movies={movies.bio} />
                    </div>
                </div>
            )}
        </>
    )
}
