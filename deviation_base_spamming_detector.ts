import type { IFDeviationBaseSpammmingDetector } from "./common/interface";
import { Queue } from "./common/queue";
import type { DeviationSpamAnalysisResult } from "./common/type";
import { getMinMax } from "./common/util";

export class DeviationBaseSpammmingDetector implements IFDeviationBaseSpammmingDetector {
    epsilon: number;
    timestampQueue: Queue<number>;
    timeoutLimit: number // milli-seocnd

    constructor(epsilon: number = 0.01, timeoutLimit: number = 5000) {
        this.epsilon = epsilon
        this.timestampQueue = new Queue<number>()
        this.timeoutLimit = timeoutLimit
    }

    private settimeoutQueue(timestamp: number) {
        setTimeout(() => {
            if(this.timestampQueue.asArray()[0] == timestamp) { // 분석 대상은 queue에서 제거 되기에, 조건문 필요
                this.timestampQueue.get()
            }
            // remove timeout element ( not save )
        }, this.timeoutLimit);
    }

    collectTimestamp(timestamp: number): void {
        this.timestampQueue.put(timestamp)
        this.settimeoutQueue(timestamp)
    }

    getRepetitionScoreArray(): DeviationSpamAnalysisResult {
        
        const calculateTarget = this.timestampQueue.asArray() // return queue elements to array
        const delayArray = this.getDelayArray()
        const reptitionScoreArray: Array<number> = []

        let avgScore: number = 0;
        delayArray.forEach(value => avgScore += value)
        avgScore = avgScore / delayArray.length

        for (let i = 0; i < delayArray.length; i++) {
            if (delayArray.length - 1 == i) {
                break
            }

            const { min, max } = getMinMax(delayArray[i], delayArray[i + 1])
            let _score = 1 - (max - min) / (avgScore + this.epsilon)
            reptitionScoreArray.push(_score)
        }
        this.timestampQueue.clear()
        return {
            epsilon: this.epsilon,
            timeoutLimit: this.timeoutLimit,
            messageTimestamps: calculateTarget,
            delays: delayArray,
            repetitionScores: reptitionScoreArray
        }
    }


    getDelayArray(): Array<number> {
        const timestamps: Array<number> = this.timestampQueue.asArray()
        const delayArray: Array<number> = []

        if (timestamps.length < 2) {
            throw `getDelayArray function is called when timestamps.length < 2`
        }

        for(let i = 0; i < timestamps.length; i++) {
            if (timestamps.length - 1 == i) {
                break
            }
            const { min, max } = getMinMax(timestamps[i], timestamps[i + 1])
            delayArray.push(max - min)
        }

        return delayArray
    }

}