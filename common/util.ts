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