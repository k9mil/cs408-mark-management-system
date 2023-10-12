import React from 'react'

import { render } from "@testing-library/react";
import { expect, test } from '@jest/globals';

import Component from "../src/components/ui/component";

test("Renders the Component and extract correct div value", () => {
    const { getByText } = render(<Component />);
    const component = getByText('Component');

    expect(component).toBeDefined();
});