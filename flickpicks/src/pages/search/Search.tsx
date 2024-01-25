import { Button, Input, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader, Select, SelectItem, useDisclosure } from "@nextui-org/react";
import { useEffect, useState } from "react";
import { AiFillFilter, AiOutlineArrowDown, AiOutlineArrowUp, AiOutlineSearch } from "react-icons/ai";
import { getCall, postCall } from "../../components/api";
import Loading from "../../components/Loading";
import MovieCard from "../../components/MovieCard";

type Movie = {
    id: number,
    title: string,
    poster_path: string,
    release_date: string,
    genres: string,
    isFavorite: boolean
}
type Filter = {
    genres: string[],
    status: string[],
    language: string[],
    sortBy: string,
    ascending: boolean
}

const genres = [
    "Action",
    "Comedy",
    "Thriller",
    "Crime",
    "Drama",
    "Animation",
    "Adventure",
    "Horror",
    "Romance",
    "Science Fiction",
    "Music",
    "War",
    "Fantasy",
    "Mystery",
]

const languages = [
    "hi",
    "kn",
    "te",
]
const statuses = [
    "Released",
    "In Production",
    "Planned",
    "Post Production",
    "Canceled",
]
const sortBy = [
    "popularity",
    "release_date",
    "vote_average",
]



const Filter = ({ isOpen, onOpenChange, onFilter, filter, setFilter }: {
    isOpen: boolean,
    onOpenChange: () => void,
    onFilter: () => void,
    filter: Filter,
    setFilter: (filter: Filter) => void
}) => {



    return (
        <>
            <Modal isOpen={isOpen} backdrop="blur" size="2xl" onOpenChange={onOpenChange}>
                <ModalContent>
                    {(onClose) => (
                        <>
                            <ModalHeader className="flex flex-col gap-1">Modal Title</ModalHeader>
                            <ModalBody>
                                <div className="flex flex-col gap-3">
                                    <div className="flex gap-2">
                                        <Select
                                            placeholder="Genre"
                                            className="max-w-xs md:w-1/2"
                                            size="sm"
                                            selectionMode="multiple"
                                            selectedKeys={filter.genres}
                                            onSelectionChange={(keys) => {
                                                setFilter({ ...filter, genres: Array.from(keys) as string[] })
                                            }}
                                        >
                                            {genres.map((genre) => {
                                                return <SelectItem key={genre}>{genre}</SelectItem>
                                            })}

                                        </Select>
                                        <Select
                                            placeholder="Languages"
                                            className="max-w-xs md:w-1/2"
                                            size="sm"
                                            selectionMode="multiple"
                                            selectedKeys={filter.language}
                                            onSelectionChange={(keys) => {
                                                setFilter({ ...filter, language: Array.from(keys) as string[] })
                                            }}
                                        >
                                            {languages.map((genre) => {
                                                return <SelectItem key={genre}>{genre}</SelectItem>
                                            })}

                                        </Select>
                                    </div>
                                    <div className="flex gap-2">
                                        <Select
                                            placeholder="Status"
                                            className="max-w-xs md:w-1/2"
                                            size="sm"
                                            selectionMode="multiple"
                                            selectedKeys={filter.status}
                                            onSelectionChange={(keys) => {
                                                setFilter({ ...filter, status: Array.from(keys) as string[] })
                                            }}
                                        >
                                            {statuses.map((genre) => {
                                                return <SelectItem key={genre}>{genre}</SelectItem>
                                            })}

                                        </Select>
                                        <div className="max-w-xs flex gap-1 md:w-1/2 items-center">
                                            <Select
                                                placeholder="SortBy"
                                                size="sm"
                                                selectedKeys={[filter.sortBy]}
                                                selectionMode="single"
                                                onSelectionChange={(keys) => {

                                                    setFilter({ ...filter, sortBy: (Array.from(keys) as string[])[0] });
                                                }}
                                            >
                                                {sortBy.map((genre) => {
                                                    return <SelectItem key={genre} value={genre}>{genre}</SelectItem>
                                                })}

                                            </Select>
                                            <Button size="lg" isIconOnly onClick={() => setFilter({ ...filter, ascending: !filter.ascending })}>
                                                {filter.ascending ? <AiOutlineArrowUp className="text-2xl" /> : <AiOutlineArrowDown className="text-2xl" />}
                                            </Button>
                                        </div>
                                    </div>

                                </div>
                            </ModalBody>
                            <ModalFooter>
                                <Button color="danger" variant="light" onPress={() => {
                                    setFilter({
                                        genres: [],
                                        language: [],
                                        status: [],
                                        sortBy: "popularity",
                                        ascending: false
                                    })
                                }}>
                                    Clear Filter
                                </Button>
                                <Button color="primary" onPress={() => {
                                    onFilter();
                                    onClose();
                                }}>
                                    Filter
                                </Button>
                            </ModalFooter>
                        </>
                    )}
                </ModalContent>
            </Modal >
        </>
    );
}


export default function Search() {
    const [query, setQuery] = useState("");
    const [loading, setLoading] = useState(false)
    const [movies, setMovies] = useState([] as Movie[])
    const { isOpen, onOpen, onOpenChange } = useDisclosure();
    const [filter, setFilter] = useState<Filter>({
        genres: [],
        language: [],
        status: [],
        sortBy: "popularity",
        ascending: false
    })
    const handleSearch = async () => {
        if (query.trim() == "") {
            return;
        }
        setLoading(true);
        const data = await getCall(`movies?q=${query.trim()}`);
        setMovies(data.movies);
        setLoading(false);
    }
    const getMovies = async () => {
        setLoading(true)
        const data = await getCall('movies');
        setLoading(false)
        setMovies(data.latest);
    }
    const onFilter = async () => {
        setLoading(true);
        const data = await postCall("movies/filter", filter);
        setMovies(data.movies);
        setLoading(false);
    }

    useEffect(() => {
        getMovies()
    }, [])


    return (
        <>
            <Filter onFilter={onFilter} isOpen={isOpen} filter={filter} setFilter={setFilter} onOpenChange={onOpenChange} />
            <div className="flex gap-3 my-4  max-w-full w-[70%] mx-auto">
                <Button size="lg" isIconOnly onClick={onOpen}>
                    <AiFillFilter className="text-2xl" />
                </Button>
                <div className="flex-1">
                    <Input type="search" isRequired value={query} onChange={(e) => setQuery(e.target.value)} size="sm" radius="md" className="" placeholder="Search Movie" variant="flat" />
                </div>
                <Button size="lg" isIconOnly onClick={handleSearch}>
                    <AiOutlineSearch className="text-2xl" />
                </Button>
            </div>
            {loading && <Loading />}
            {!loading && <div className="grid lg:grid-cols-5 md:grid-cols-4 sm:grid-cols-3 grid-cols-2 sm:px-8 px-4 my-4 gap-3">
                {movies.length == 0 && !loading && <div className="col-span-full text-xl my-5 text-center">No Movie found</div>}
                {movies.map((movie: Movie, i: number) => {
                    return <MovieCard key={i} movie={movie} />
                })}
            </div>}
        </>
    )
}