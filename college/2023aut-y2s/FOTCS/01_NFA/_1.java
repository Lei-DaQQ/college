import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;
import java.util.Stack;

/*
q1 0 q1
q1 1 q1
q1 1 q2
q2 0 q3
q2 # q3
q3 1 q4
q4 0 q4
q4 1 q4
###

q1
q4
101

*/
public class _1 {

    public static void main(String[] args) {
        NFA nfa = new NFA();
        Scanner scanner = new Scanner(System.in);

        // Continue taking input until three '###' are entered
        while (true) {
            System.out.print("Enter a string to match (type '###' to exit the program): ");
            String inputString = scanner.nextLine().trim();

            if (inputString.equals("###")) {
                break;
            } else {
                System.out.println("The string is: " + inputString);

                boolean isMatch = nfa.matchString(inputString);
                System.out.println("String " + (isMatch ? "matches" : "does not match") + " the NFA.\n");
            }
        }
        // scanner.close();

    }
}

class NFA {
    private Set<String> states;
    private Set<Character> symbols;
    private String beginState; // Initial state of the NFA
    private Set<String> endStates; // Set of accepting (end) states
    private Transition transitions;

    public String getBeginState() {
        return beginState;
    }

    public void setBeginState(String beginState) {
        this.beginState = beginState;
    }

    public Set<String> getEndStates() {
        return endStates;
    }

    public void setEndStates(Set<String> endStates) {
        this.endStates = endStates;
    }

    public void getBeginAndEnd() {
        Scanner scanner = new Scanner(System.in);

        // Prompt user for the initial state, repeat until a non-empty input is provided
        do {
            System.out.print("Enter the initial state: ");
            beginState = scanner.nextLine().trim();

        } while (beginState.isEmpty());
        System.out.println("The initial state is: " + beginState);

        // Prompt user for the accepting (end) states, repeat until at least one state
        // is provided
        do {
            System.out.print("Enter the accepting (end) states separated by spaces: ");
            String endStateInput = scanner.nextLine().trim();

            if (endStateInput.isEmpty()) {
                System.out.println("Please enter at least one accepting state.");
                continue;
            }

            String[] endStateArray = endStateInput.split(" ");
            endStates = new HashSet<>(Arrays.asList(endStateArray));
        } while (endStates.isEmpty());
        // scanner.close();
        System.out.println("The accepting (end) states: " + endStates);

    }

    public NFA() {
        transitions = new Transition();
        transitions.getTransition();
        this.getBeginAndEnd();
    }

    private Set<String> epsilonClosure(Set<String> states) {
        Set<String> visited = new HashSet<>();
        Stack<String> stack = new Stack<>();

        for (String state : states) {
            stack.push(state);
            visited.add(state);
        }

        while (!stack.isEmpty()) {
            String currentState = stack.pop();
            Set<String> epsilonTransitions = transitions.getNextStates(currentState, '#');

            if (epsilonTransitions.size() != 0) {
                for (String nextState : epsilonTransitions) {
                    if (!visited.contains(nextState)) {
                        stack.push(nextState);
                        visited.add(nextState);
                    }
                }
            }
        }

        states.addAll(visited);
        return states;
    }

    public void printMatchingInfo(int charIndex, String currentState, char inputSymbol, Set<String> nextStateSet,
            Set<String> epsilonClosureSet, int length) {
        System.out.println("--------------------------------------------");
        System.out.println("Recognizing the " + (charIndex + 1) + "th character: " + inputSymbol);
        System.out.println("Current state: " + currentState);

        for (String nextState : nextStateSet) {
            System.out.print(
                    "Recognizing character: " + inputSymbol + ", transitioning to new state: " + nextState + ", ");
            System.out.println("Adding state: " + nextState + ".");
        }

        System.out.print(
                "Recognizing the current character: " + inputSymbol + ", ε-closure obtained: " + epsilonClosureSet);

        if (charIndex == length - 1) {
            boolean isAccepted = epsilonClosureSet.stream().anyMatch(endStates::contains);
            if (isAccepted)
                System.out.print(
                        "\nThe ε-closure set contains accepting states, this string is accepted by the state machine.");
            else
                System.out.print("\nThis branch failed to match.");

        }
        System.out.println("\n--------------------------------------------");
    }

    public void printAcceptance(boolean isAccepted) {
        System.out.println("The ε-closure set " + (isAccepted ? "contains" : "does not contain") + " accepting states "
                + endStates + ", this string "
                + (isAccepted ? "is" : "is not") + " accepted by the state machine");
        System.out.println("------------------END-------------------");
    }

    // start to search:
    public boolean matchString(String input) {
        int length = input.length();
        Set<String> currentStates = new HashSet<>();
        currentStates.add(beginState);
        epsilonClosure(currentStates);

        boolean endStatesIntersect = false;

        for (int charIndex = 0; charIndex < input.length(); charIndex++) {
            char symbol = input.charAt(charIndex);
            Set<String> nextStates = new HashSet<>();
            Set<String> epsilonClosureStates = new HashSet<>();

            // start to trans
            for (String currentState : currentStates) {
                Set<String> nextStateSet = transitions.getNextStates(currentState, symbol);
                if (nextStateSet != null) {
                    nextStates.addAll(nextStateSet);
                }

                for (String nextState : nextStates) {
                    Set<String> nextStateCopy = new HashSet<>(Arrays.asList(nextState));
                    epsilonClosureStates.addAll(epsilonClosure(nextStateCopy));

                }

                endStatesIntersect = epsilonClosureStates.stream().anyMatch(endStates::contains);
                printMatchingInfo(charIndex, currentState, symbol, nextStates, epsilonClosureStates, length);

            }
            currentStates = epsilonClosureStates;

        }

        printAcceptance(endStatesIntersect);

        return endStatesIntersect;

    }

} // class NFA

class Transition {

    private Map<Map<String, Character>, Set<String>> transitions;

    public Transition() {
        transitions = new HashMap<>();
    }

    public void addTransition(String fromState, char symbol, String toState) {
        Map<String, Character> transitionKey = new HashMap<>();
        transitionKey.put(fromState, symbol);
        transitions.computeIfAbsent(transitionKey, k -> new HashSet<>()).add(toState);
    }

    public void getTransition() {

        Scanner scanner = new Scanner(System.in);

        System.out.println(
                "Please input the NFA transition rules in the format 'start symbol end', \nand use '#' to represent epsilon.");
        System.out.println("Example1: q1 a q2");
        System.out.println("Example2: q1 # q3");
        System.out.println("Enter '###' to finish input.");

        String input;
        while (true) {
            System.out.print("Input transition rule: ");
            input = scanner.nextLine().trim();
            if (input.equals("###")) {
                break;
            }
            String[] parts = input.split(" ");
            if (parts.length == 3) {
                String fromState = parts[0];
                char symbol = parts[1].charAt(0);
                String toState = parts[2];
                this.addTransition(fromState, symbol, toState);
                System.out.println("Transition added: " + fromState + " -(" + symbol + ")-> " + toState);
            } else {
                System.out.println("Invalid input format. Please use the format 'start symbol end'.");
            }
        }

        // scanner.close();

    }

    public Set<String> getNextStates(String currentState, char inputSymbol) {
        Set<String> nextStates = new HashSet<>();
        for (Map.Entry<Map<String, Character>, Set<String>> entry : transitions.entrySet()) {
            Map<String, Character> transitionKey = entry.getKey();
            if (transitionKey.containsKey(currentState) && transitionKey.get(currentState) == inputSymbol) {
                nextStates.addAll(entry.getValue());
            }
        }
        return nextStates;
    }
}
