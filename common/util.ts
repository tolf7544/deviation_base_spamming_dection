import type { MinMax } from "./type"
/**
 * 
 * @param num_1 
 * @param num_2 
 * @returns \{
            "min": number,
            "max": number
        }

    수치가 같을 경우는 고려하지 않음
 */
export function getMinMax(num_1: number, num_2: number): MinMax {
    if(num_1 > num_2) {
        return {
            "min": num_2,
            "max": num_1
        }
    } else {
        return {
            "min": num_1,
            "max": num_2
        }
    }
}

export function min(a: number, b: number) {
    if(a > b) return b
    else return a
}

export function max(a: number, b: number) {
    if(a > b) return a
    else return b
}


export function conditionalProbability(p_1: number, p_2: number) {
    return (p_1 * p_2) / p_2
    
}