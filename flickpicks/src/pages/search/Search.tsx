import { Button, Input } from "@nextui-org/react";
import { useEffect, useState } from "react";
import { AiFillFilter, AiOutlineSearch } from "react-icons/ai";
import { getCall } from "../../components/api";
import Loading from "../../components/Loading";
import MovieCard from "../../components/MovieCard";

type Movie = {
    id: number,
    title: string,
    poster_path: string,
    release_date: string,
    genres: string,
    isFavorite:boolean
}

export default function Search(){
    const [query,setQuery] = useState("");
    const [loading, setLoading] = useState(false)
    const [movies, setMovies] = useState([] as Movie[])

    

    const handleSearch = async() => {
        console.log(query);
        setLoading(true);
        const data =await getCall(`movies?q=${query}`);
        setMovies(data.movies);
        setLoading(false);

      }
    const getMovies = async () => {
        setLoading(true)
        const data = await getCall('movies');
        setLoading(false)
        setMovies(data.latest);
    }

    useEffect(() => {
        getMovies()
    }, [])

    
    return (
    <>
        <div className="flex gap-3 my-4  max-w-full w-[70%] mx-auto">
            <Button size="lg" isIconOnly>
                <AiFillFilter className="text-2xl"/>
            </Button>
            <div className="flex-1">
                <Input type="search" value={query} onChange={(e)=>setQuery(e.target.value)} size="sm" radius="md"  className=""  placeholder="Search Movie" variant="flat"/>
            </div>
            <Button size="lg" isIconOnly onClick={handleSearch}>
                <AiOutlineSearch className="text-2xl"/>
            </Button>
        </div>
        {loading && <Loading />}
        {!loading && <div className="grid lg:grid-cols-5 md:grid-cols-4 sm:grid-cols-3 grid-cols-2 sm:px-8 px-4 my-4 gap-3">
                {movies.length == 0 && !loading && <div className="col-span-full text-xl my-5 text-center">No favorites yet</div>}
                {movies.map((movie: Movie, i: number) => {
                    return <MovieCard key={i} movie={movie}  />
                })}
            </div>}
    </>
    )
}