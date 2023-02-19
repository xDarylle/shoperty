import React from "react"
import { StarRating } from 'components'
export default function ProductCard({ imageUrl, props }) {
    return (
        <a href={`/product/${props.id}`} >
            <div className="m-1 group flex flex-col w-full lg:w-72 bg-white drop-shadow overflow-hidden hover:outline outline-primary z-10">
                <div className="h-52 md:h-60 overflow-hidden">
                    <img className="object-cover w-full h-full" src={imageUrl} alt={`${props.productName}`} />
                </div>
                <div className="flex flex-col justify-between p-3 h-24 gap-y-1">
                    <div className="text-base text-gray-700 truncate h-14 ">{props.productName}</div>
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-end ">
                        <span className="text-base text-lg md:text-2xl text-primary ">₱{props.price.toLocaleString()}</span>
                        <div className="flex flex-row gap-x-1 items-center text-sm text-gray-500 w-32">
                            <StarRating percent={props.ratings} name={props.id}/>
                            <p>({props.sold})</p>
                        </div>
                    </div>
                </div>
            </div>
        </a>
    )
}