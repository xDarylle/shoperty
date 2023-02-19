import React, { useEffect, useState } from "react";
import { Star } from 'react-feather'
import { axiosRequest } from "api"
import swal from "sweetalert2"

export default function RateProduct({ status, setStatus, props }) {
    const [hover, setHover] = useState(undefined)
    const [selected, setSelected] = useState(undefined)

    useEffect(() => {
        setSelected(props.rating - 1)
    }, [props])

    const setRating = async () => {
        const data = {
            product: props.id,
            rating: selected ? selected + 1 : 0
        }

        const response = await axiosRequest.post("/api/v1/product/ratings", data)
        const { status } = response
        if (status === 200) {
            swal.fire({
                title: "Thank you for rating this product",
                icon: "success",
            })
            setStatus(false)
        }
    }

    return (
        <div className={`justify-center items-center w-screen h-screen overflow-x-hidden overflow-y-auto fixed top-0 left-0 right-0 z-50 bg-black/40 ${status}`}>
            <div className="flex-col gap-y-7 flex bg-white px-10 py-5 justify-center items-center text-center rounded-lg">
                <p className="text-xl">Rate this product</p>
                <div className="flex flex-row w-full justify-center">
                    {[...Array(5).keys()].map((_, index) => {
                        return (
                            <button className="text-primary/80 px-1"
                                onMouseEnter={() => { setHover(index); setSelected(undefined) }}
                                onMouseLeave={() => { setHover(undefined) }}
                                onClick={() => { setSelected(index) }}
                                key={index}
                            >
                                <Star size={40} fill={selected >= index ? "#EB4800" : index <= hover ? "#EB4800" : "white"} />
                            </button>
                        );
                    })}
                </div>
                <div className="flex flex-row justify-between w-full ">
                    <button className="rounded bg-primary text-white w-20 py-1" onClick={setRating}>Save</button>
                    <button className="rounded border border-black  w-20 py-1" onClick={() => setStatus(false)}>Cancel</button>
                </div>
            </div>
        </div>
    );
}