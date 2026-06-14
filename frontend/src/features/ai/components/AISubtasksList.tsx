type Props = {
    subtasks: string[];
};

export default function AISubTasksList({
    subtasks,
}: Props) {
    return (
        <ul>
            {subtasks.map((task, index) => (
                <li key={index}>
                    {task}
                </li>
            ))}
        </ul>
    );
}