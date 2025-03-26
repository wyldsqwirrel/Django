import React, { useState } from "react";
import { useDrag, useDrop } from "react-dnd";

const Field = ({ field, index, moveField }) => {
  const [, ref] = useDrag({
    type: "field",
    item: { index },
  });

  const [, drop] = useDrop({
    accept: "field",
    hover: (draggedItem) => {
      if (draggedItem.index !== index) {
        moveField(draggedItem.index, index);
        draggedItem.index = index;
      }
    },
  });

  return (
    <div ref={(node) => ref(drop(node))} className="draggable-field">
      {field.name} ({field.type})
    </div>
  );
};

const DragDropFormBuilder = () => {
  const [fields, setFields] = useState([
    { name: "First Name", type: "text" },
    { name: "Email", type: "email" },
    { name: "Phone Number", type: "phone" },
  ]);

  const moveField = (fromIndex, toIndex) => {
    const updatedFields = [...fields];
    const [movedField] = updatedFields.splice(fromIndex, 1);
    updatedFields.splice(toIndex, 0, movedField);
    setFields(updatedFields);
  };

  return (
    <div>
      <h2>Drag & Drop Form Builder</h2>
      <div className="form-builder">
        {fields.map((field, index) => (
          <Field key={index} field={field} index={index} moveField={moveField} />
        ))}
      </div>
    </div>
  );
};

export default DragDropFormBuilder;
