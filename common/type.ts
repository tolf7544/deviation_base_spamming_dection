export type MessageTimestampElement = {
    timestamp: string; // UTC ms format
    message: string;
}

export type DeviationSpamAnalysisResult = {
    epsilon: number,
    timeoutLimit: number
    messageTimestamps: Array<number>,
    delays: Array<number>,
    score_1: Array<number>,
    score_2: number
}
export type BidirectionalScoreResult = {
    delays: Array<number>,
    scores: Array<number>
}

export type ConditionalPScoreResult = BidirectionalScoreResult
export type ConditionalPSpamAnalysisResult = DeviationSpamAnalysisResult


export type MinMax = {
    "min": number,
    "max": number
} 