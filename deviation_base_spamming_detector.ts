import type { IFDeviationAnalysis } from "./common/interface";
import { Queue } from "./common/queue";
import type { BidirectionalScoreResult, DeviationSpamAnalysisResult } from "./common/type";
import { conditionalProbability, getMinMax, max, min } from "./common/util";

export class DeviationBaseSpammmingDetector implements IFDeviationAnalysis {
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

    getBidirectionalScore(): BidirectionalScoreResult {
        const delays = this.getDelays()
        const scores = Array<number>();
        for (let i = 0; i < delays.length; i++) {
            if(delays.length-1 == i) {
                break
            }
            let _min = min(delays[i], delays[i+1])
            let _max = max(delays[i], delays[i+1])
            scores.push(_min/_max)
        }

        return {
            delays: delays,
            scores: scores
        }
    }

    getAnalysisResult(): DeviationSpamAnalysisResult {
        
        const calculateTarget = this.timestampQueue.asArray() // return queue elements to array
        const {delays, scores} = this.getBidirectionalScore()
        const reptitionScoreArray: Array<number> = []
        let totalScore:number = 1;
        let CPScore: number = 1;

        for (let i = 0; i < scores.length; i++) {
            if(i+1 == scores.length) {
                break
            }
            CPScore = conditionalProbability(scores[i+1], scores[i])
        }

        console.log("-", CPScore)

        for (let i = 0; i < delays.length; i++) {
            if (delays.length - 1 == i) {
                break
            }
                
            const { min, max } = getMinMax(delays[i], delays[i + 1])
            const deviation = max - min
            const avg = CPScore + this.epsilon
            let _score = 0
            console.log("-", deviation)
            console.log("-", avg)
            if(deviation > avg) {
                _score = 0
            } else {
                _score = deviation / avg
            }
            console.log("-", _score)
            totalScore *= _score
            
            reptitionScoreArray.push(_score)
            
        }
        this.timestampQueue.clear()
        return {
            epsilon: this.epsilon,
            timeoutLimit: this.timeoutLimit,
            messageTimestamps: calculateTarget,
            delays: delays,
            score_1: reptitionScoreArray,
            score_2: 1 - totalScore
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

