import type { Interface } from "readline";
import type { BidirectionalScoreResult, ConditionalPScoreResult, ConditionalPSpamAnalysisResult, DeviationSpamAnalysisResult } from "./type";
import type { Queue } from "./queue";

export interface IFTestPromptProcesser {
    collectionSize: number
    readline: Interface


    setMainSection(i: number): void
    displaySection({ messageTimestamps, epsilon, timeoutLimit, delays, score_1, score_2 }: DeviationSpamAnalysisResult ): void
}
export interface IFSpammmingDetector {
    epsilon: number,
    timestampQueue: Queue<number>
    timeoutLimit: number // milli-seocnd https://currentmillis.com/

    collectTimestamp(timestamp: number): void
    getDelays(): Array<number>
}
export interface IFConditionalProbabilityAanlysis extends IFSpammmingDetector {
    getAnalysisResult(): ConditionalPSpamAnalysisResult
    getConditionalProbability(): ConditionalPScoreResult
}

export interface IFDeviationAnalysis extends IFSpammmingDetector {
    getAnalysisResult(): DeviationSpamAnalysisResult
    getBidirectionalScore(): BidirectionalScoreResult
}

export interface IFQueue<T> { 
    put(data:T): IFQueue<T>
    get(): T | undefined
    display(): void
    asArray(): Array<T>
    clear(): Array<T>
}

export interface IFStatistics {
    mean(group: Array<number>): number
    median(group: Array<number>): number
    max(group: Array<number>): number
    min(group: Array<number>): number
    
    covariance(group_1: Array<number>, group_1_mean: number | null, group_2: Array<number>, group_2_mean: number | null): number

}