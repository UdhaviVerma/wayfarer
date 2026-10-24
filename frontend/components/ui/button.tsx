import { ButtonHTMLAttributes } from 'react';
import clsx from 'clsx';

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'default' | 'outline';
};

export function Button({ className, variant = 'default', ...props }: Props) {
  return (
    <button
      className={clsx(
        'inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-medium transition',
        variant === 'default' && 'bg-primary text-white hover:opacity-90',
        variant === 'outline' && 'border border-border bg-transparent hover:bg-card',
        className,
      )}
      {...props}
    />
  );
}
