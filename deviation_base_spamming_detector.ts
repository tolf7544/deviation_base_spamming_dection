import type { IFDeviationBaseSpammmingDetector } from "./common/interface";
import { Queue } from "./common/queue";
import type { DeviationSpamAnalysisResult } from "./common/type";
import { getMinMax } from "./common/util";

export class DeviationBaseSpammmingDetector implements IFDeviationBaseSpammmingDetector {
    epsilon: number;
    timestamp: Date;
    timestampQueue: Queue<number>;
    timeoutLimit: number // milli-seocnd

    constructor(epsilon: number = 0.01, timeoutLimit: number = 5000) {
        this.epsilon = epsilon
        this.timestamp = new Date()
        this.timestampQueue = new Queue<number>()
        this.timeoutLimit = timeoutLimit
    }

    private settimeoutQueue() {
        setTimeout(() => {
            this.timestampQueue.get()
            // remove timeout element ( not save )
        }, this.timeoutLimit);
    }

    collectTimestamp(timestamp: number): void {
        this.timestampQueue.put(timestamp)
        this.settimeoutQueue()
    }

    getRepetitionScoreArray(): DeviationSpamAnalysisResult {
        const calculateTarget = this.timestampQueue.asArray()
        const delayArray = this.getDelayArray()
        const reptitionScoreArray: Array<number> = []

        let avgScore: number = 0;
        delayArray.forEach(value => avgScore += value)
        
        for (let i = 0; i < delayArray.length; i++) {
            if (delayArray.length - 1 == i + 1) {
                break
            }
            const { min, max } = getMinMax(delayArray[i], delayArray[i + 1])
            let _score = (max - min) / (avgScore + this.epsilon)
            reptitionScoreArray.push(_score)
        }
        
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

        for (let i = 0; i < timestamps.length; i++) {
            if (timestamps.length - 1 == i + 1) {
                break
            }
            const { min, max } = getMinMax(timestamps[i], timestamps[i + 1])
            delayArray.push(max - min)
        }

        return delayArray
    }

}