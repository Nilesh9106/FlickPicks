import { useEffect, useState } from "react"
import { getCall } from "../../components/api"
import MovieCard from "../../components/MovieCard"
import Loading from "../../components/Loading"
import { Button } from "@nextui-org/react"

type Movie = {
    id: number,
    title: string,
    poster_path: string,
    release_date: string,
    genres: string,
    isFavorite: boolean
}

type History = {
    id: number,
    movie: Movie,
    added: string,
}

export default function History() {
    const [loading, setLoading] = useState(false)
    const [Histories, setHistories] = useState([] as History[])

    const fetchHistories = async () => {
        setLoading(true)
        const data = await getCall(`user/history`);
        setLoading(false)
        if (data?.status == "success") {
            setHistories(data.histories)
        }
    }
    const clearHistory = async () => {
        if (!confirm("Are you sure you want to clear your history?")) return
        setLoading(true)
        const data = await getCall("user/clearHistory")
        if (data?.status == "success") {
            setHistories([])
        }
        setLoading(false);
    }

    useEffect(() => {
        fetchHistories()
    }, [])

    return (
        <>
            {loading && <Loading />}
            <div className="flex px-10 py-3">
                <Button isDisabled={Histories.length == 0} onClick={clearHistory} color="danger" variant="flat">
                    Clear History
                </Button>
            </div>
            <div className="grid lg:grid-cols-5 md:grid-cols-4 grid-cols-3 p-5 gap-3">
                {Histories.length == 0 && !loading && <div className="col-span-full text-xl my-5 text-center">No Histories yet</div>}
                {Histories.map((movie: History, i: number) => {
                    return <MovieCard key={i} movie={movie.movie} />
                })}
            </div>
        </>
    )
}
