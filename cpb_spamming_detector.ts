import type { IFConditionalProbabilityAanlysis } from "./common/interface";
import { Queue } from "./common/queue";
import type { DeviationSpamAnalysisResult, BidirectionalScoreResult, ConditionalPSpamAnalysisResult, ConditionalPScoreResult } from "./common/type";
import { conditionalProbability, getMinMax, max, min } from "./common/util";

export class CPSpammingDetector implements IFConditionalProbabilityAanlysis {
    epsilon!: number;
    timestampQueue: Queue<number>;
    timeoutLimit: number;
    
    constructor( timeoutLimit: number = 5000) {
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

    getAnalysisResult(): ConditionalPSpamAnalysisResult {
        const calculateTarget = this.timestampQueue.asArray()
        const {delays, scores} = this.getConditionalProbability()
        const score = conditionalProbability(scores[1], scores[0])
        this.timestampQueue.clear()
        return {
            epsilon: NaN,
            timeoutLimit: this.timeoutLimit,
            messageTimestamps: calculateTarget,
            delays: delays,
            score_1: scores,
            score_2: score
        }
    }

    getConditionalProbability(): ConditionalPScoreResult {
        const delays = this.getDelays()
        const delayScores = Array<number>();

        for (let i = 0; i < delays.length; i++) {
            if(delays.length-1 == i) {
                break
            }
            let _min = min(delays[i], delays[i+1])
            let _max = max(delays[i], delays[i+1])
            delayScores.push(_min/_max)
        }

        return {
            delays: delays,
            scores: delayScores
        }
    }

    getDelays(): Array<number> {
        const timestamps: Array<number> = this.timestampQueue.asArray()
        const delays: Array<number> = []

        if (timestamps.length < 2) {
            throw `getDelayArray function is called when timestamps.length < 2`
        }

        for(let i = 0; i < timestamps.length; i++) {
            if (timestamps.length - 1 == i) {
                break
            }
            const { min, max } = getMinMax(timestamps[i], timestamps[i + 1])
            delays.push(max - min)
        }

        return delays
    }
    
}