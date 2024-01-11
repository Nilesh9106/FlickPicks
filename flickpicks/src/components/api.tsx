import axios from "axios"
import { toast } from "react-toastify";


export const postCall = async (endPoint: string, data: unknown) => {

    try {
        const response = await axios.post(`${import.meta.env.VITE_API_URI}${endPoint}`, data, {
            headers: localStorage.getItem('token') ? {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            } : {}
        });
        return response.data;
    } catch (error) {
        // console.log(error);
        if (axios.isAxiosError(error)) {
            if (error.response?.status === 401) {
                localStorage.removeItem('token')
                localStorage.removeItem('user')
                toast.error("Session expired")
                window.location.href = '/auth'
            }
            toast.error(error.response?.data?.message ?? "Something went wrong")
        } else {
            toast.error("Something went wrong")
        }
        return { status: "error" }
    }
}

export const getCall = async (endPoint: string) => {
    try {
        const response = await axios.get(`${import.meta.env.VITE_API_URI}${endPoint}`, {
            headers: localStorage.getItem('token') ? {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            } : {}
        });
        return response.data;
    } catch (error) {
        console.log(error);
        if (axios.isAxiosError(error)) {
            if (error.response?.status === 401) {
                localStorage.removeItem('token')
                localStorage.removeItem('user')
                toast.error("Session expired")
                window.location.href = '/auth'
            }
            toast.error(error.response?.data?.message ?? "Something went wrong")
        } else {
            toast.error("Something went wrong")
        }
    }
}

export const tmdbGetCall = async (endPoint: string, param?: string) => {
    try {
        const response = await axios.get(`https://api.themoviedb.org/3/${endPoint}?api_key=${import.meta.env.VITE_TMDB_KEY}&${param}`);
        return response.data;
    } catch (error) {
        console.log(error);
        if (axios.isAxiosError(error)) {
            console.error(error.response?.data?.message ?? "Something went wrong")
        } else {
            console.error("Something went wrong")
        }
    }
}