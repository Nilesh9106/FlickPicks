import { useEffect, useState } from "react"
import { getCall } from "../../components/api"
import MovieCard from "../../components/MovieCard"
import Loading from "../../components/Loading"

type Movie = {
    id: number,
    title: string,
    poster_path: string,
    release_date: string,
    genres: string,
}
type Favorites = {
    id: number,
    movie: Movie,
    added: string
}

export default function Favorites() {
    const [loading, setLoading] = useState(false)
    const [favorites, setFavorites] = useState([] as Favorites[])

    const fetchFavorites = async () => {
        setLoading(true)
        const data = await getCall(`movies/favorites`);
        setLoading(false)
        if (data?.status == "success") {
            setFavorites(data.movies)
            console.log(data.movies);

        }
    }

    useEffect(() => {
        fetchFavorites()
    }, [])

    return (
        <>
            {loading && <Loading />}
            <div className="grid lg:grid-cols-5 md:grid-cols-4 sm:grid-cols-3 grid-cols-2 sm:px-8 px-4 my-4">
                {favorites.length == 0 && !loading && <div className="col-span-full text-xl my-5 text-center">No favorites yet</div>}
                {favorites.map((movie: Favorites, i: number) => {
                    return <MovieCard key={i} movie={movie.movie} />
                })}
            </div>
        </>
    )
}
